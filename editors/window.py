"""
window.py - Window class for line-oriented display editors.

Each window instance displays a range of lines from a text buffer.
"""

from datetime import datetime # for timestamp, used for testing
import display
from update import Op

def clip(iline, first, last):
    'return iline limited to range first .. last inclusive'
    return min(max(first, iline), last)

class Window(object):
    """
    Window class for line-oriented display editors.
    Displays a range of lines (the segment) from a text buffer.
    Includes a status line with information about the buffer.
    Has a line called dot where text insertions etc. occur.
    May display a cursor-like marker to indicate dot.
    """

    nupdates = 0 # diagnostic, used by update_status_info

    def __init__(self, buf, win_1, win_h, ncols):
        """
        Initialize window, given its text buffer, location, and dimensions
        buf - text buffer displayed in this window, must have:
          buf.lines: list of strings, buf.S(): returns index of last line,
          buf.dot: index of current line, buf.npage: n of lines for paging cmds
          buf.unsaved: boolean, buf.name: string
        win_1 -line number on display of first buffer line shown in this window
        win_h - number of lines in this window, including status region
        ncols - maximum number of characters in a line
        """
        self.buf = buf
        # Initialize but never update self.dot here, this window might not be current
        self.dot = self.buf.dot 
        # status_h is height of status region in lines, usually 1
        self.status_h = 1 # height (lines) of window status region(status line)
        self.resize(win_1, win_h, ncols) # assigns self.win_1 .win_h .ncols
        # self.seg_1,seg_n are indices in buffer of 1st,last lines in window
        self.seg_1 = 1 # index in buffer of first line displayed in window
        self.seg_n = min(self.win_hl, self.buf.S()) # index of last line
        self.dot_i = 0 # line number on display of this window's dot, 0 not visible
        self.marker_ch = '' # character that marker overwrites
        self.marker_chx = '' # same as marker_ch except when that is blank
        self.dot_i0 = 0 # previous value of dot_i
        self.marker_ch0 = '' # previous value of marker_ch

        self.first = 0    # first line printed on window during this update
        self.nprinted = 0 # n of lines printed on window during this update

    # assign window dimenions: self.win_1 win_h win_hl status_1 ncols buf.npage
    
    # called by __init__ and also at other time
    def resize(self, win_1, win_h, ncols):
        'Assign, recalculate window dimensions'
        self.win_1 = win_1 # line number on display of 1st line of this window
        self.win_h = win_h # number of lines in this window including status
        self.ncols = ncols # max number of chars in a line
        # There are also edd.py global win_h: total lines in all windows
        self.win_hl = self.win_h - self.status_h #window lines excluding status
        # status_1 is line num on display of 1st line of status region
        self.status_1 = self.win_1 + self.win_hl # first line after buffer text
        self.buf.npage = self.win_hl # page size for classic ed z paging command
        # seg_1, seg_n assigned in set_segment, called from update_window.
        # seg_1, seg_n are also reassigned when dot moves.

    # report segment position: top, near bottom, at bottom, dot elsewhere,moved
    # FIXME?  Make dot an argument to all these, rather than using self.dot?

    def near_buf_top(self):
        'dot is in top half of segment at beginning of buffer that fits in window.'
        # // is python 3 floor division
        return (self.dot <= self.win_hl//2 or self.buf.S() <= self.win_hl)

    def near_buf_bottom(self):
        'dot is in bottom half of segment at end of buffer that fits in window.'
        return (self.buf.S() - self.dot < self.win_hl//2 and
                self.buf.S() >= self.win_hl)

    def at_bottom_line(self):
        'dot is at last line in buffer and is last line in full window.'
        seg_h = self.seg_n - self.seg_1 + 1 # lines in segment, maybe < win_hl
        return (self.dot == self.buf.S() and self.seg_n == self.buf.S() 
                and seg_h == self.win_hl)

    def dot_elsewhere(self):
        'dot lies outside segment of buffer visible in window'
        return ((not self.seg_1 <= self.dot <= self.seg_n) 
                if self.dot else False)
    
    def dot_moved(self):
        'dot moved to a different line in the buffer (than dot_i0)'
        return self.dot_i != self.dot_i0

    def position_segment(self):
        """
        Given dot, assign self.seg_1: index in buffer of top line in window.
        Center window on dot if possible,otherwise show top or bottom of buffer
        Uses line addresses in buffer self.dot self.buf.S()
         also window height self.win_hl
        """
        # FIXME?  Make dot an argument rather than using self.dot?
        if self.near_buf_top(): # first line at top of window
            self.seg_1 = 1  
        elif self.near_buf_bottom(): # last line at bottom of window
            self.seg_1 = self.buf.S() - (self.win_hl - 1)
        else: # dot is centered in window
            self.seg_1 = self.dot - self.win_hl//2 # floor division

    def find_end(self):
        """
        Compute bottom of segment of buffer that is visible in window.
        Assign self.seg_n: index in buffer of last line shown in window.
        Depends on self.seg_1 computed in position_segment (above), call that first
         also depends on height self.win_hl, and possibly line address self.buf.S()
        Center window on dot if possible,otherwise show top or bottom of buffer
        """
        if self.near_buf_top(): # first line is at top of window
            self.seg_n = min(self.win_hl, self.buf.S())
        elif self.near_buf_bottom(): # last line is at bottom of window
            self.seg_n = self.buf.S()
        else: # dot is centered in window
            self.seg_n = self.seg_1 + (self.win_hl - 1)

    def find_dot(self):
        """
        Compute location of dot (the current line) in window.
        Assign self.dot_i: line number on display where self.dot appears
         if it is visible, otherwise assign to self.dot_i to 0.
        Depends on self.seg_1 computed in position_segment (above), call that first.
        Also uses line address in buffer self.dot, 
         window location on display self.win_1, window height self.win_hl
        Also update self.marker_ch, the marker character,
         because we may need to erase it later.
        """
        self.dot_i0 = self.dot_i
        self.marker_ch0 = self.marker_ch
        if self.buf.empty() or self.dot_elsewhere():
            self.dot_i = 0
            self.marker_ch = ''
        else:
            self.dot_i = self.win_1 + (self.dot - self.seg_1)
            # self.marker_ch is char at start of line that marker overwrites.
            line = self.buf.lines[self.dot]
            self.marker_ch = line[0] if line else ''
            # self.marker_chx ensures marker on space or empty line is visible.
            self.marker_chx = (' ' if self.marker_ch in ('',' ','\n') 
                               else self.marker_ch)

    def adjust_segment(self, update):
        """
        Adust self.dot .seg_1 .seg_n so that same contents remain at same
        positions in window even when line numbers change due to deletes
        or inserts above.  Compare to management of mark in Buffer.
        """
        if update.op == Op.insert:  
            if self.dot >= update.start: # FIXME? update.destination
                self.shift(update.nlines)
        elif update.op == Op.delete:
            if update.start <= self.dot <= update.end:
                self.shift(self.buf.dot - self.dot) # so dot + shift == buf.dot
            elif self.dot >= update.start and self.dot >= update.end:
                self.shift(-update.nlines)

    # display (parts of) window

    def render_lines(self, first, last):
        """
        Print lines in buffer numbered first through last.
        Assumes cursor already positioned at first line.
        """
        i = -1
        for i, line in enumerate(self.buf.lines[first:last+1]):
            print(line.rstrip()[:self.ncols-1], end=' ') # remove \n, truncate
            display.kill_line()
            print()
        return i+1 # n printed, less than first:last+1 if end of buf

    def render_segment(self, open_line=False):
        """
        Start on win_1 line, display buffer lines self.seg_1 .. self.seg_n 
        If space remains in window, pad with empty lines to self.win_h
        If in insert mode (not command_mode),open line where text will be typed
        """
        # FIXME similar to update_lines below - just keep one
        # lines in segment, usually same as self.win_hl, less if small buffer
        seg_h = self.seg_n - self.seg_1 + 1 
        # n of padding empty lines at window bottom, > 0 when small buffer
        blank_h = self.win_hl - seg_h   
        display.put_cursor(self.win_1,1)  # cursor to window top
        if open_line: # open line at dot to insert new text
            self.render_lines(self.seg_1 +(1 if self.at_bottom_line() else 0),
                               self.dot) # leave space at dot
            display.kill_whole_line() # open line to insert new text
            print() # next line
            self.render_lines(self.dot+1, 
                               self.seg_n-(0 if self.near_buf_top() else 1))
        else:
            self.render_lines(self.seg_1, self.seg_n)
        for iline in range(blank_h if not open_line else blank_h - 1):
            display.kill_whole_line()
            print()

    def render_status_prefix(self):
        "Print information about window's buffer in its status line."
        s1 = self.status_1  # line number of status bar on display
        unsaved = '-----**-     ' if self.buf.unsaved else '--------     ' # 13
        bufname = '%-13s' % self.buf.name
        position = (' All ' if self.buf.S() <= self.win_hl else # S() is last line
                    ' Top ' if self.seg_1 == 1 else
                    ' Bot ' if self.seg_n == self.buf.S() else
                    ' %2.0f%% ' % (100*self.dot/(len(self.buf.lines)-1))) # %% prints %
        linenums = '%-14s' % ('L%d/%d ' % (self.dot, self.buf.S()))
        display.put_render(s1, 0, unsaved, display.white_bg)
        display.put_render(s1, 13, bufname, display.bold, display.white_bg)
        display.put_render(s1, 26, position, display.white_bg)
        display.put_render(s1, 31, linenums, display.white_bg)

    def render_status(self):
        "Print information about window's buffer in its status line."
        self.render_status_prefix()
        timestamp = datetime.strftime(datetime.now(),' %H:%M:%S -') # 10 char
        s1 = self.status_1  # line number of status bar on display
        display.put_render(s1, 45, '-'*(self.ncols-(45+10)), display.white_bg)
        display.put_render(s1, self.ncols-10, timestamp, display.white_bg)

    def render_status_info(self, update):
        "Print diagnostic and debug information in the status line."
        self.render_status_prefix()
        s1 = self.status_1   # line number of status bar on display
        Window.nupdates += 1 # ensure at least this changes in status line
        update_info = '%3d %3s s:%3d e:%3d d:%3d n:%3d,%3d %3d' % \
            (Window.nupdates, str(update.op)[3:6],
             update.start, update.end, update.destination, update.nlines,
             self.first, self.nprinted)
        display.put_render(s1, 40, update_info, display.white_bg)
        display.kill_line()
        self.first = 0    # reset after each update
        self.nprinted = 0 

    def render_marker(self):
        """
        Display cursor-like marker at start of line to indicate dot
        when terminal cursor is elsewhere (at command line etc.)
        """
        if self.buf.empty():
            display.put_render(self.win_1, 1, ' ', display.white_bg)
        else:
            display.put_render(self.dot_i, 1, self.marker_chx, display.white_bg)

    def erase_marker(self):
        'At start of line, replace marker with saved character'
        if self.dot_i0 == 0: # was empty buffer
            display.put_render(self.win_1, 1, ' ', display.clear)
        else:
            ch = self.marker_ch0 if not self.marker_ch0 == '\n' else ' '
            display.put_render(self.dot_i0, 1, ch, display.clear)
            
    def put_insert_cursor(self):
        'Position cursor at start of open line after dot for i(nsert) a c cmds'
        if self.buf.empty():
            iline = self.win_1  
        else:
            iline = self.dot_i + (0 if self.at_bottom_line() else 1)
        display.put_cursor(iline, 1) # open line after dot

    def put_update_cursor(self):
        'Position cursor at start of dot itself for in-line edits.'
        if self.buf.empty():
            iline = self.win_1  
        else:
            iline = self.dot_i
        display.put_cursor(iline, 1)

    def update(self, open_line=False):
        """
        Position and render window contents including text and status line,
        but NOT its marker or cursor.
        """
        # do not call position_segment() here, can cause distracting jumps
        self.find_end()
        self.find_dot() 
        self.render_segment(open_line)
        self.render_status()
        # No self.put_insert_cursor or render_marker, caller must do it.

    ### New and revised methods used by update.op cases in new frame module ###

    # Naming - Here we use win_i arg for line number on display,
    #   BUT in frame.py win_i is index of current window in windows list - !!??

    def bottom(self):
        'Line number on display of last content line in window (not status line).'
        return self.win_1 + self.win_hl - 1

    def buf2win(self, seg_i):
        'Line number on display of seg_i in buffer.'
        return self.win_1 + (seg_i - self.seg_1)
 
    def empty_line(self, seg_i):
        'True when line number seg_i in buffer is empty, or is just \n'
        return self.buf.lines[seg_i] in ('','\n')

    def ch0(self, seg_i):
        'First character in line seg_i in buffer, or space if line is empty'
        return ' ' if self.empty_line(seg_i) else self.buf.lines[seg_i][0]

    def set_marker(self, win_i, seg_i):
        'Set marker on display line number win_i which shows buffer line seg_i'
        # FIXME?  Handle empty buffer here or in caller?
        display.put_render(win_i, 1, self.ch0(seg_i), display.white_bg)

    def clear_marker(self, win_i, seg_i):
        'Clear marker from display line win_i which shows buffer line seg_i'
        display.put_render(win_i, 1, self.ch0(seg_i), display.clear)

    def scroll(self, nlines):
        """
        Move segment of buffer displayed in window by nlines (pos or neg),
        but leave dot unchanged so window contents appear to scroll.
        """
        last = self.buf.S()
        self.seg_1 = clip(self.seg_1 + nlines, 1, last)
        self.seg_n = clip(self.seg_n + nlines,  1, last)

    def shift(self, nlines):
        """
        Move segment of buffer displayed in window by nlines (pos or neg),
        and shift dot also so window contents appear the same.
        """
        self.scroll(nlines)
        self.dot = clip(self.dot + nlines, 1, self.buf.S())

    def open_line(self, win_i):
        'Make line empty at line number win_i on display'
        # FIXME - omit guard - don't call this when out-of-range - let it crash
        #if self.win_1 <= win_i <= self.win_1 + self.win_h - 2:
        display.put_cursor(win_i, 1)
        display.kill_whole_line()

    def clear_lines(self, first, last):
        """
        Clear consecutive consecutive lines from first through last in window.
        Cursor must be positioned at first line already.
        """
        for i in range(first,last+1): # unempty if reached end of buffer
            display.kill_whole_line()
            print()

    def update_lines(self, first, seg_i, last=0):
        """
        Write lines in window starting at line numbered first on the display,
        to the bottom of the window, or to line numbered last if arg present.
        Lines come from self.buf starting at its line seg_i.
        """
        self.first = first if not self.first else self.first
        # FIXME similar to render_segment above - just keep one
        last = last if last else self.bottom()
        # FIXME - omit guard - don't call this when out-of-range - let it crash
        #if (self.win_1 <= first <= last and 1 <= seg_i <= self.buf.S()):
        self.seg_n = seg_i + (last - first)
        display.put_cursor(first, 1)
        self.nprinted += self.render_lines(seg_i, self.seg_n)
        icursor = first + self.nprinted
        self.clear_lines(icursor, last)

    def update_for_input(self):
        """
        Open next line and overwrite lines below.
        If at bottom of window, scroll insertion point up to the middle.
        Then place input cursor.
        """
        self.dot_i = self.buf2win(self.buf.dot)
        if self.dot_i > 0:
            display.put_render(self.dot_i, 1, self.buf.lines[self.buf.dot][0],
                               display.clear) # erase cursor at dot
        if self.dot_i >= self.win_1 + self.win_hl - 1: # at bottom of window
            self.scroll(self.win_hl//2)
            self.dot_i = self.win_1 + (self.buf.dot - self.seg_1)
            self.update_lines(self.win_1, self.buf.dot-self.win_hl//2+1, 
                             last=self.dot_i)
        self.open_line(self.dot_i+1)
        self.update_lines(self.dot_i+2, self.buf.dot+1)
