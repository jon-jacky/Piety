"""
window.py - Window class for line-oriented display editors.

Each window displays a range of lines (a segment) of a text buffer, and
also includes a final status line with information about its contents.
"""

import display

def clip(iline, first, last):
    'return iline limited to range first .. last inclusive'
    return min(max(first, iline), last)

show_diagnostics = False # on status line - for now, don't show

class Window(object):
    """
    Window class for line-oriented display editors.
    Displays a range of lines (the segment) from a text buffer.
    After the segment, displays a status line with information about contents.
    May display a marker to indicate dot, the line where commands take effect.
    """

    nupdates = 0 # diagnostic, optionally show on status line

    def __init__(self, buf, top, nlines, ncols):
        """
        Initialize window, given its text buffer, location,and dimensions
         buf - text buffer displayed in this window
         top - line number on display of first buffer line in window
         nlines - number of lines in this window, excluding status line
         ncols - maximum number of characters in a line
        """
        self.focus = False # input focus, only used in self.status_text()  
        self.buf = buf
        self.saved_dot = self.buf.dot  # to restore dot when window selected
        self.btop = 1 # index in buffer of first line displayed in window
        self.resize(top, nlines, ncols) # assigns self.top .nlines .ncols
        self.blast = self.blastline() # buffer can get out of synch

        # Diagnostics, optionally show on status line
        self.first = 0    # first line printed on window in this update
        self.nprinted = 0 # n of lines printed on window in this update

    # Helper methods, used within this class but not called by clients

    # window geometry calculations

    def bottom(self):
        'Line num. on display of bottom line in window (not status line)'
        return self.top + self.nlines - 1

    def bbottom(self):
        'Index in buffer of bottom line in window. May exceed buffer size'
        return self.btop + self.nlines - 1

    def blastline(self):
        """
        Index in buffer of last line in window, maybe not bottom of window.
        Assumes that last line in window is up-to-date with buffer size.
        """
        return min(self.bbottom(), self.buf.nlines())
 
    def statusline(self):
         "Line number on display of window's status line"
         return self.bottom() + 1

    def near_top(self, iline):
        """
        Line number in buffer iline is in
        top half of segment at beginning of buffer that fits in window.
        """
        return (iline <= self.nlines//2 or self.buf.nlines() <= self.nlines)

    def near_bottom(self, iline):
        """
        Line number in buffer iline is in
        bottom half of segment at end of buffer that fits in window.
        """
        return (self.buf.nlines() - iline < self.nlines//2 and
                self.buf.nlines() >= self.nlines)
 
    def empty_line(self, iline):
        'Line number iline in buffer is empty, or is just \n'
        return self.buf.lines[iline] in ('','\n')

    def covers(self, iline):
        'Line number iline in buffer is in range of lines covered by window.'
        return (self.btop <= iline <= self.bbottom())

    # markers

    def ch0(self, iline):
        'First character in line iline in buffer, or space if line empty'
        return ' ' if self.empty_line(iline) else self.buf.lines[iline][0]

    def put_marker(self, iline, clear=False):
        'Set or clear marker on buffer line iline, or top line if buffer empty'
        display.put_render(self.top if self.buf.empty() else self.wline(iline),
                           1, self.ch0(iline), 
                           display.clear if clear else display.white_bg)

    # adjust window positions
                           
    def shift(self, nlines):
        """
        Shift segment of buffer displayed in window by nlines (pos or neg)
        but leave its saved_dot unchanged so window contents will appear to 
        scroll when window is updated on display.
        """
        self.btop = clip(self.btop + nlines, 1, self.buf.nlines())
        self.blast = self.blastline()

    def translate(self, nlines):
        """
        Shift segment of buffer displayed in window by nlines (pos or neg)
        and also shift its saved_dot.   If nlines lines have been deleted
        or inserted elsewhere in the file, the window contents will appear
        the same when the window is updated on the display.
        """
        self.shift(nlines)
        self.saved_dot = clip(self.saved_dot + nlines, 1, self.buf.nlines())

    # update windows

    def open_line(self, wiline):
        'Make line empty at line number wiline on display'
        #if self.top <= wiline <= self.top + self.nlines-1: # omit,let it crash
        display.put_cursor(wiline, 1)
        display.kill_whole_line()

    def clear_lines(self, first, last):
        """
        Clear consecutive lines from first through last in window.
        Cursor must be positioned at first line already.
        """
        for i in range(first,last+1): # unempty if reached end of buffer
            display.kill_whole_line()
            display.next_line()

    def render_lines(self, first, last):
        """
        Print lines in buffer numbered first through last.
        Assumes cursor already positioned at first line.
        """
        i = -1
        for i, line in enumerate(self.buf.lines[first:last+1]):
            display.putstr(line.rstrip('\n')[:self.ncols]) # truncate
            display.kill_line()
            display.next_line()
        return i+1 # fewer than first:last+1 when at end of buffer

    def update_lines(self, first, iline, last=0):
        """
        Write lines in window starting at line numbered first on display,
        to bottom of the window, or to line numbered last if arg present.
        Lines come from self.buf starting at its line iline.
        """
        self.first = first if self.first == 0 else self.first
        last = last if last else self.bottom()
        blastlinenum = iline + (last - first) # might exceed $ near eob
        display.put_cursor(first, 1)
        nprinted = self.render_lines(iline, blastlinenum)
        icursor = first + nprinted
        self.nprinted += nprinted
        self.clear_lines(icursor, last)

    # status line
       
    def status_text(self):
        'Return string about window and its buffer for its status line.'
        current = '----.' if self.focus else '-----'
        readonly = '%' if self.buf.readonly else '-'
        modified = '*-     ' if self.buf.modified else '--     '
        bufname = '%-13s' % self.buf.name
        dot = self.buf.dot if self.focus else self.saved_dot
        position = (' All ' if self.buf.nlines() <= self.nlines else
                    ' Top ' if self.btop == 1 else
                    ' Bot ' if self.blast == self.buf.nlines() else
                    ' %2.0f%% ' % (100*dot/self.buf.nlines()))
        linenums = '%-14s' % ('L%d/%d ' % (dot, self.buf.nlines()))
        bufmodetext = '(%s)' % (self.buf.mode,) # 'Text' or 'Python' or ...
        bufmode = bufmodetext + '-'*(10 - len(bufmodetext))
        statustext = (current + readonly + modified + bufname + position +
                      linenums + bufmode)
        nstatus = len(statustext)
        if show_diagnostics:
            Window.nupdates += 1 # ensure at least this changes in diagnostics
            diagnostics = '  N%6d f%3d n%3d' % \
                (Window.nupdates, self.first, self.nprinted)
            nsuffix = len(diagnostics)
            npad = self.ncols - (nstatus + nsuffix)
            statustext += '-'*npad + diagnostics
        else: # show + at column 80
            npad79 = 79 - nstatus
            npad81 = self.ncols - 81
            statustext += '-'*npad79 + '+' + '-'*npad81
        return statustext[:self.ncols+1]

    def update_status_line(self, text):
        'display text on status line with white_bg'
        display.put_render(self.statusline(), 1, text, display.white_bg)

    # Methods called by clients

    # window geometry calculations

    def resize(self, top, nlines, ncols):
        """
        Assign, recalculate window dimensions
         top - line number on display of first line of window
         nlines - n of lines in window, excludling status line
         ncols - maximum number of characters in a line
        """
        self.top = top
        self.nlines = nlines
        self.ncols = ncols

    def wline(self, iline):
        'Line number on display of iline in buffer.'
        return self.top + (iline - self.btop)

    def contains(self, iline):
        'Line number iline in buffer is one of the lines present in the window'
        return (self.btop <= iline <= self.blast)

    def intersects(self, start, end):
        'Window intersects range defined by start..end'
        return (self.contains(start) or self.contains(end)
                or (start < self.btop and end > self.bbottom()))

    def samebuf(self, win):
        'True when this window differs from win but uses the same buffer'
        return (self != win and self.buf == win.buf)

    # markers

    def set_marker(self, iline):
        'Set marker on buffer line iline, or top line if buffer empty'
        self.put_marker(iline)

    def clear_marker(self, iline):
        'Clear marker from buffer line iline, or top line if buffer empty'
        self.put_marker(iline, clear=True)

    # adjust window positions

    def locate(self, destination):
        """
        Shift segment of buffer displayed in window to center on destination, 
        a line number in buffer.
        """
        if self.near_top(destination):
            self.btop = 1  
        elif self.near_bottom(destination):
            self.btop = self.buf.nlines() - (self.nlines - 1) # last page
        else: 
            self.btop = destination - self.nlines//2 # center dest. in window
        self.blast = self.blastline()

    # update windows

    def render_from(self, start):
        """
        Write lines in window, starting at line number start in buffer.
        Update window status line.
        """
        self.update_lines(self.wline(start), start)
        self.update_status()

    def refresh(self):
        'Render all the lines in the window, update status line'
        self.render_from(self.btop)

    def update(self, destination=None):
        """
        Locate window at destination (line in buffer) then update window.
        Default destination is dot.
        """
        if destination is None:
            destination=self.buf.dot
        self.locate(destination)
        self.refresh()

    def modify(self, start, end):
        """
        Update focus window after insert lines to start..end
        OR after delete lines above start.
        For delete, pass same iline for start and end.
        """
        if self.contains(end):  # window already contains new dot
            self.render_from(start)
        else:
            self.update()

    def mutate_lines(self, start, end):
        """
        Update focus window after some lines in range start..end changed.
        Similar to render_from above, but can be more efficient: can
        update a band of lines within the window, not all the way to bottom.
        """        
        top = max(start, self.btop)
        self.update_lines(self.wline(top), top, 
                       last=self.wline(end))
        self.update_status()

    def mutate(self, start, end):
        """
        Update focus window and move marker after some lines in range changed.
        Similar to modify() above, but can be more efficient: can
        update a band of lines within the window, not all the way to bottom.
        """
        if self.contains(end):
            self.mutate_lines(start, end)
        else:
            self.update()

    def update_for_input(self):
        """
        For use with ed input mode: a i c.  Text at dot is already up-to-date.
        Open next line and overwrite lines below.
        If at bottom of window, scroll insertion point up to the middle.
        """
        wdot = self.wline(self.buf.dot) # line on display where dot appears
        if wdot > 0:
            self.clear_marker(self.buf.dot)
        if wdot >= self.bottom():
            self.shift(self.nlines//2)
            wdot = self.wline(self.buf.dot)
            self.update_lines(self.top, self.btop, last=wdot)
        self.open_line(wdot+1)
        self.update_lines(wdot+2, self.buf.dot+1)
        self.update_status()

    def put_cursor_for_input(self, column=1):
        """ 
        For use with ed input mode: a i c commands.
        Place input cursor for insert after update_for_input, above
        """
        wdot = self.wline(self.buf.dot)
        display.put_cursor(wdot+1, column)

    def adjust_insert(self, start, end):
        """
        Update window that is *not* focus window after insert into its buffer.
        start, end are line numbers *after* insert is executed in buffer.
        ed i() inserts text *before* dot, so start == buf.dot before insert.
        """
        nlines = end - start + 1 # positive, text below insert moves down
        # buffer was empty before insert
        if self.saved_dot == 0:
            self.saved_dot = self.buf.dot
            self.update()
        # window precedes inserted lines
        elif self.blast < start:
            pass
        # window includes start of inserted lines
        elif self.covers(start):
            # saved_dot follows start of inserted lines
            if self.saved_dot >= start:
                self.saved_dot = self.saved_dot + nlines
            self.update(destination=self.saved_dot)
        # window follows inserted lines
        elif self.btop >= start:
            self.shift(nlines)
        self.update_status()

    def adjust_delete(self, start, end, destination):
        """
        Update window that is *not* focus window after delete from its buffer.
        start, end - line numbers *before* delete is executed in buffer.
        destination - first unchanged line *after* delete executed in buf.
        destination may differ from start if we delete through end of buffer,
        see buffer d() method.
        """
        nlines = -(end - start + 1) # negative, text below insert moves up
        # window preceded deleted lines
        if self.blast < start:
            pass
        # window included deleted lines
        elif self.intersects(start, end):
            # saved_dot preceded deleted lines
            if self.saved_dot < start:
                pass
            # saved_dot followed deleted lines
            elif self.saved_dot > end:
                self.saved_dot = self.saved_dot + nlines
            # saved_dot was in deleted lines
            else:
                self.saved_dot = destination
            self.update(destination=self.saved_dot)
        # window followed deleted lines
        elif self.btop > end:
            self.translate(nlines)
        self.update_status()

    # status line

    def update_status(self):
        'display status text on status line'
        self.update_status_line(self.status_text())
        self.first = 0    # diagnostics, reset after each update
        self.nprinted = 0

