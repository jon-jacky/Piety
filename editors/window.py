"""
window.py - Window class for line-oriented display editors.

Each window instance displays a range of lines from a text buffer.
"""

import display
from datetime import datetime # for timestamp, used for testing

class Window(object):
    """
    Window class for line-oriented display editors.
    A window displays a range of lines (segment) from a text buffer.
    A window includes a status line with information about the buffer.
    A window may display a cursor to indicate the current line, called dot.
    """
    def __init__(self, buf, win_1, win_h, ncols):
        """
        Initialize window, given its text buffer, location, and dimensions
        buf - text buffer displayed in this window, must have:
          buf.lines: list of strings, buf.S(): returns index of last line,
          buf.dot: current line, buf.npage: n of lines for paging commands
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
        self.seg_n = min(self.win_hl, self.buf.S()) # index last line
        self.cursor_i = None # line number of current buffer's dot on display
        self.cursor_ch = None # character that cursor overwrites
        self.cursor_chx = None # same as cursor_ch except when that is blank
        self.cursor_i0 = None # previous value of cursor_i
        self.cursor_ch0 = None # previous value of cursor_ch

    def resize(self, win_1, win_h, ncols):
        'Assign, recalculate window dimensions'
        self.win_1 = win_1 # line number on display of 1st line of this window
        self.win_h = win_h # number of lines in this window including status
        self.ncols = ncols # max number of chars in a line
        # There are also edd.py global win_h: total lines in all windows
        self.win_hl = self.win_h - self.status_h #window lines excluding status
        # status_1 is line num on display of 1st line of status region
        self.status_1 = self.win_1 + self.win_hl # first line after buffer text
        self.buf.npage = self.win_hl # page size for z Z cmds
        # seg_1, seg_n assigned in locate_segment, called from update_window.
        # seg_1, seg_n are also reassigned when dot moves.

    def near_buffer_top(self):
        'dot is in top half of segment at beginning of buffer that fits in window.'
        # // is python 3 floor division
        return (self.dot <= self.win_hl//2 or self.buf.S() <= self.win_hl)

    def near_buffer_bottom(self):
        'dot is in bottom half of segment at end of buffer that fits in window.'
        return (self.buf.S() - self.dot < self.win_hl//2 and
                self.buf.S() >= self.win_hl)

    def at_bottom_line(self):
        'dot is at last line in buffer and is last line in full window.'
        seg_h = self.seg_n - self.seg_1 + 1 # lines in segment, maybe < win_hl
        return (self.dot == self.buf.S() and self.seg_n == self.buf.S() 
                and seg_h == self.win_hl)

    def locate_segment(self):
        """
        Compute segment of buffer that is visible in window.
        Assign self.seg_1 - index in buffer of first line shown in window.
          also self.seg_n - index in buffer of last line shown in window.
        Center window on dot if possible,otherwise show top or bottom of buffer
        """
        if self.near_buffer_top(): # first line at top of window
            self.seg_1 = 1  
            self.seg_n = min(self.win_hl, self.buf.S())
        elif self.near_buffer_bottom(): # last line at bottom of window
            self.seg_1 = self.buf.S() - (self.win_hl - 1)
            self.seg_n = self.buf.S()
        else: # dot is centered in window
            self.seg_1 = self.dot - self.win_hl//2 # floor division
            self.seg_n = self.seg_1 + (self.win_hl - 1)

    def display_lines(self, first, last):
        """
        Print lines in buffer numbered first through last
        starting at current cursor position - assumes cursor already positioned
        """
        for line in self.buf.lines[first:last+1]: # slice, upper limit excluded
            # remove \n, truncate don't wrap
            print(line.rstrip()[:self.ncols-1], end=' ') 
            display.kill_line() # erase from cursor to end
            print() # advance to next line

    def display_window(self, command_mode):
        """
        Start on win_1 line, display buffer lines self.seg_1 .. self.seg_n 
        If space remains in window, pad with empty lines to self.win_h
        If in insert mode (not command_mode), open line where text will be typed
        """
        # lines in segment, usually same as self.win_hl, less if small buffer
        seg_h = self.seg_n - self.seg_1 + 1 
        # n of padding empty lines at window bottom, > 0 when small buffer
        blank_h = self.win_hl - seg_h   
        display.put_cursor(self.win_1,1)  # cursor to window top
        if command_mode:
            self.display_lines(self.seg_1, self.seg_n)
        else: # insert mode, open line at dot to insert new text
            self.display_lines(self.seg_1 +(1 if self.at_bottom_line() else 0),
                               self.dot) # leave space at dot
            display.kill_whole_line() # open line to insert new text
            print() # next line
            self.display_lines(self.dot+1, 
                               self.seg_n - (0 if self.near_buffer_top() else 1))
        for line in range(blank_h if command_mode else blank_h - 1):
            display.kill_whole_line()
            print()

    def display_status(self):
        "Print information about window's buffer in its status line."
        s1 = self.status_1  # line number of status bar on display
        unsaved = '-----**-     ' if self.buf.unsaved else '--------     '
        bufname = '%-13s' % self.buf.name
        position = (' All ' if self.buf.S() <= self.win_hl else # S() is last line
                    ' Top ' if self.seg_1 == 1 else
                    ' Bot ' if self.seg_n == self.buf.S() else
                    ' %2.0f%% ' % (100*self.dot/(len(self.buf.lines)-1))) # %% prints %
        linenums = '%-14s' % ('L%d/%d ' % (self.dot, self.buf.S()))
        timestamp = datetime.strftime(datetime.now(),' %H:%M:%S -') # 10 ch w/margin
        display.put_render(s1, 0, unsaved, display.white_bg)
        display.put_render(s1, 13, bufname, display.bold, display.white_bg)
        display.put_render(s1, 26, position, display.white_bg)
        display.put_render(s1, 31, linenums, display.white_bg)
        display.put_render(s1, 45, '-'*26, display.white_bg)
        display.put_render(s1, self.ncols-10, timestamp, display.white_bg)

    def cursor_elsewhere(self):
        'dot lies outside segment of buffer visible in window'
        return ((not self.seg_1 <= self.dot <= self.seg_n) 
                if self.dot else False)
    
    def cursor_moved(self):
        'Cursor moved to a different line in the buffer (than cursor_i0)'
        return self.cursor_i != self.cursor_i0

    def locate_cursor(self):
        """
        Update self.cursor_i to line number of dot on display
         if it is visible, else assign to 0.
        Also update self.cursor_ch, the cursor character,
         because we will need to erase it later.
        """
        self.cursor_i0 = self.cursor_i # save previous values
        self.cursor_ch0 = self.cursor_ch
        # buffer not empty, don't count empty first line at index 0
        if len(self.buf.lines)-1: 
            # self.cursor_ch is char at start of line that cursor overwrites
            cursor_line = self.buf.lines[self.dot]
            self.cursor_ch = cursor_line[0] if cursor_line else ''
            # To ensure cursor on space or empty line is visible, 
            #  use self.cursor_chx
            self.cursor_chx = (' ' if self.cursor_ch in ('',' ','\n') 
                               else self.cursor_ch)
            self.cursor_i = self.win_1 + (self.dot - self.seg_1)
            self.cursor_i = (self.cursor_i 
                             if (self.win_1 <= self.cursor_i 
                                 <= self.win_1 + self.win_hl -1)
                             else 0)
        else:
            self.cursor_i = 0
            self.cursor_ch = ''

    def display_cursor(self):
        'Display cursor at start of display line'
        if self.cursor_i:
            display.put_render(self.cursor_i, 1, self.cursor_chx, display.white_bg)
        elif self.dot == 0:
            # special case, empty buffer,  _ cursor at window ulc
            display.put_render(self.win_1, 1, ' ', display.white_bg) # no blink

    def erase_cursor(self):
        'At start of previous display line, replace cursor with saved char.'
        if self.cursor_i0:
            ch = self.cursor_ch0 if not self.cursor_ch0 == '\n' else ' '
            display.put_render(self.cursor_i0, 1, ch, display.clear)
        elif self.dot == 0: # empty buffer, special case, cursor at window ulc
            display.put_render(self.win_1, 1, ' ', display.clear)
            
    def set_insert_cursor(self):
        'Position cursor at start of open line after dot for insert append change cmds.'
        if self.cursor_i == 0: # empty buffer, special case, cursor at window top
            line = self.win_1  
        else:
            line = self.cursor_i + (0 if self.at_bottom_line() else 1)
        display.put_cursor(line, 1) # open line after dot

    def update_window(self, command_mode):
        'Locate and display the window including its status line and cursor.'
        self.locate_segment() # assign new self.seg_1, self.seg_n
        self.locate_cursor()  # *re*assign new self.cursor_i, cursor_ch
        self.display_window(command_mode)
        self.display_status()
        # No self.set_insert_cursor or display_cursor, caller must do it.
