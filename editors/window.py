"""
window.py - Window class for line-oriented display editors.

Each window displays a range of lines (a segment) of a text buffer.
All updates here involve a whole line or group of lines from a buffer.

Updates within a line are handled by the console or edsel modules,
which use the display module to write and update that line
directly on the display, without using this window module.
The line being edited by console or edsel is not yet part of a buffer
so it cannot be handled by this module.
"""

import display

def clip(iline, first, last):
    'return iline limited to range first .. last inclusive'
    return min(max(first, iline), last)

# command_mode is True when entering/editing/executing commands
# on the command line and printing output in the scrolling region,
# command_mode is False when entering/editing text in a display window.
# It is possible to edit buffers and manage windows from
# the command line, so display window contents can change a lot
# in command_mode.

# When command_mode is True, the terminal cursor where the user
# types input is in the command region,
# so we display a marker in a display window to show where
# commands will take effect.   The marker appears in the focus window
# at the first character of the current line, dot.
# When command_mode is False (in display editing modes),
# the marker is not displayed, because instead the terminal cursor
# where the user types input appears in the focus window
# at point (the character position where insertions and deletions
# take effect).

# command_mode here is assigned in the frame module once at startup:
#  window.command_mode = (lambda: mode == Mode.command)
# after this assignment, window.command_mode() follows frame.mode
# even though the window module does not import the frame module.

command_mode = (lambda: True) # will be reassigned in frame module

show_diagnostics = False # on status line - for now, don't show

class Window(object):
    """
    Window class for line-oriented display editors.
    Displays a range of lines (the segment) from a text buffer.
    May display a marker to indicate dot, the line where commands take effect.
    May be followed by a status line with information about the buffer.
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
        self.focus = False # True when this window has the input focus
        self.buf = buf
        self.saved_dot = self.buf.dot  # to restore dot when window selected
        self.btop = 1 # index in buffer of first line displayed in window
        self.resize(top, nlines, ncols) # assigns self.top .nlines .ncols
        self.blast = self.blastline() # buffer can get out of synch

        # Diagnostics, optionally show on status line
        self.first = 0    # first line printed on window in this update
        self.nprinted = 0 # n of lines printed on window in this update

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

    def contains(self, iline):
        'Line number iline in buffer is one of the lines present in the window'
        return (self.btop <= iline <= self.blast)

    def covers(self, iline):
        'Line number iline in buffer is in range of lines covered by window.'
        return (self.btop <= iline <= self.bbottom())

    def intersects(self, start, end):
        'Window intersects range defined by start..end'
        return (self.contains(start) or self.contains(end)
                or (start < self.btop and end > self.bbottom()))

    # ch0 etc. used for marker, see explanation in comment near top of file.
    # The marker, when displayed, appears in the first column of dot.

    def ch0(self, iline):
        'First character in line iline in buffer, or space if line empty'
        return ' ' if self.empty_line(iline) else self.buf.lines[iline][0]

    def put_marker(self, iline, clear=False):
        'Set or clear marker on buffer line iline, or top line if buffer empty'
        display.put_render(self.top if self.buf.empty() else self.wline(iline),
                           1, self.ch0(iline), 
                           display.clear if clear else display.white_bg)
        
    def set_marker(self, iline):
        'Set marker on buffer line iline, or top line if buffer empty'
        self.put_marker(iline)

    def clear_marker(self, iline):
        'Clear marker from buffer line iline, or top line if buffer empty'
        self.put_marker(iline, clear=True)

    def scroll(self, nlines):
        """
        Move segment of buffer displayed in window by nlines (pos or neg)
        but leave dot unchanged so window contents appear to scroll.
        """
        self.btop = clip(self.btop + nlines, 1, self.buf.nlines())
        self.blast = self.blastline()

    def shift(self, nlines):
        """
        Move segment of buffer displayed in window by nlines (pos or neg)
        and shift saved_dot also so window contents appear the same.
        This is only meaningful for the windows without input focus.
        """
        self.scroll(nlines)
        self.saved_dot = clip(self.saved_dot + nlines, 1, self.buf.nlines())

    def locate_segment(self, iline):
        """
        Given line number in buffer iline, prepare to position window by
        assigning self.btop, index in buffer of top line in window.
        """
        if self.near_top(iline):
            self.btop = 1  
        elif self.near_bottom(iline):
            self.btop = self.buf.nlines() - (self.nlines - 1) # last page
        else: 
            self.btop = iline - self.nlines//2 # center iline in window
        self.blast = self.blastline()

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
            display.putstr(line.rstrip()[:self.ncols]) # remove \n, truncate
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

    def update_from(self, iline):
        'Write lines in window starting at line number iline in buffer'
        self.update_lines(self.wline(iline), iline)
        if self.focus and command_mode():
            # self has focus, mark self.buf.dot not self.saved_dot
            self.set_marker(self.buf.dot)
        self.update_status()

    def update(self):
        'Write all lines in window'
        self.update_from(self.btop)

    def move_update(self, iline):
        'Move window to show buffer line iline then update window'
        self.locate_segment(iline)
        self.update()

    def reupdate(self):
        'Move window to show its buf.dot then update window'
        self.move_update(self.buf.dot)

    def locate(self, origin, destination):
        'Update window after dot moves from origin to destination'
        if self.contains(destination):
            if self.focus and command_mode():
                self.clear_marker(origin)
                self.set_marker(destination)
            self.update_status()
        else:
            self.reupdate()

    def insert(self, origin, start, end):
        'Update window after insert lines from origin to start..end'
        if self.contains(end):
            if origin > 0:
                self.clear_marker(origin)
            self.update_from(start)
        else:
            self.reupdate()

    def delete(self, destination):
        'Update window after delete lines above destination'
        if self.contains(destination): # window already contains new dot
            self.update_from(destination)
        else:
            self.reupdate() 

    def mutate_lines(self, start, destination):
        'Update window after some lines in range start..destination changed'
        top = max(start, self.btop)
        self.update_lines(self.wline(top), top, 
                       last=self.wline(destination))
        self.update_status()

    def mutate(self, origin, start, destination):
        'Update window and move marker after some lines in range changed'
        if self.contains(destination):
            self.clear_marker(origin)
            self.mutate_lines(start, destination)
            self.set_marker(destination)
        else:
            self.reupdate()

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
        modetext = '(%s)' % (self.buf.mode,)
        mode = modetext + '-'*(10 - len(modetext))
        statustext = (current + readonly + modified + bufname + position +
                      linenums + mode)
        nstatus = len(statustext)
        Window.nupdates += 1 # ensure at least this changes in diagnostics
        diagnostics = '  N%6d f%3d n%3d' % \
            (Window.nupdates, self.first, self.nprinted)
        nsuffix = len(diagnostics)
        suffix = diagnostics if show_diagnostics else '-'*nsuffix
        nstrut = self.ncols - (nstatus + nsuffix)
        statustext += '-'*nstrut + suffix
        return statustext

    def update_status_line(self, text):
        'display text on status line with white_bg'
        display.put_render(self.statusline(), 1, text, display.white_bg)

    def update_status(self):
        'display status text on status line'
        self.update_status_line(self.status_text())
        self.first = 0    # diagnostics, reset after each update
        self.nprinted = 0
       
# The following methods are only used with input mode

    def update_for_input(self):
        """
        Open next line and overwrite lines below.
        If at bottom of window, scroll insertion point up to the middle.
        """
        wdot = self.wline(self.buf.dot) # line on display where dot appears
        if wdot > 0:
            self.clear_marker(self.buf.dot)
        if wdot >= self.bottom():
            self.scroll(self.nlines//2)
            wdot = self.wline(self.buf.dot)
            self.update_lines(self.top, self.btop, last=wdot)
        self.open_line(wdot+1)
        self.update_lines(wdot+2, self.buf.dot+1)
        self.update_status()

    def put_cursor_for_input(self, column=1):
        'Place input cursor for insert after update_for_input, above'
        wdot = self.wline(self.buf.dot)
        display.put_cursor(wdot+1, column)

# The following methods are only used with multiple windows

    def samebuf(self, win):
        'True when this window differs from win but uses the same buffer'
        return (self != win and self.buf == win.buf)

    def set_focus(self):
        'Set input focus to this window'
        self.focus = True
        self.buf.dot = self.saved_dot
        self.set_marker(self.buf.dot)

    def release_focus(self):
        'Release input focus from this window'
        self.focus = False
        self.saved_dot = self.buf.dot
        self.clear_marker(self.saved_dot)

    def adjust_insert(self, start, end, destination):
        """
        After insert, adjust segment visible in a window without input focus,
        to keep lines shown in that window the same so no update is needed.
        """
        # start, end are line numbers *after* insert is executed in buffer.
        # ed i() inserts text *before* dot, so start == buf.dot before execute.
        # destination == end, last inserted line *after* insert executed in buf
        nlines = end - start + 1
        if self.saved_dot == 0:  # buffer was empty
            self.saved_dot = self.buf.dot
            self.move_update(self.saved_dot)
            self.update_status()
        elif self.covers(start):
            if self.saved_dot >= start:
                self.saved_dot = self.saved_dot + nlines
            self.move_update(self.saved_dot)
            self.update_status()
        elif self.btop >= start:
            self.shift(nlines)
            self.update_status()
        elif self.blast < start:
            self.update_status() # xx% nn/mm in status line changes
        else:
            pass # should be unreachable! status line doesn't update

    def adjust_delete(self, start, end, destination):
        """
        After delete, adjust segment visible in a window without input focus,
        to keep lines shown in that window the same so no update is needed.
        """
        # start, end are line numbers *before* delete is executed in buffer.
        # destination is first unchanged line *after* delete executed in buf.
        nlines = -(end - start + 1)
        if self.intersects(start, end):
            if self.saved_dot < start:
                pass
            elif self.saved_dot > end:
                self.saved_dot = self.saved_dot + nlines
            else:
                self.saved_dot = destination
            self.move_update(self.saved_dot)
            self.update_status()
        elif self.btop > end:
            self.shift(nlines)
            self.update_status()
        elif self.blast < start:
            self.update_status() # xx% nn/mm in status line changes
        else:
            pass # should be unreachable! status line doesn't update
