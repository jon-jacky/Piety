"""
window.py - Window class for line-oriented display editors.

Each window instance displays a range of lines from a text buffer.
"""

from datetime import datetime # for timestamp, used for testing
import math # for math.ceil
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

    nupdates = 0 # diagnostic, used by render_status_info

    def __init__(self, buf, top, nlines, ncols):
        """
        Initialize window, given its text buffer, location, and dimensions
        buf - text buffer displayed in this window, must have:
          buf.lines: list of strings, buf.S(): returns index of last line,
          buf.dot: index of current line, buf.npage: n of lines for paging cmds
          buf.unsaved: boolean, buf.name: string
        top -line number on display of first buffer line shown in this window
        nlines - number of lines in this window, excluding status line
        ncols - maximum number of characters in a line
        """
        self.current = False # True when this window is the current window
        self.buf = buf
        self.saved_dot = self.buf.dot 
        self.btop = 1 # index in buffer of first line displayed in window
        self.resize(top, nlines, ncols) # assigns self.top .nlines .ncols

        # DIAGNOSTICS
        self.first = 0    # first line printed on window during this update
        self.nprinted = 0 # n of lines printed on window during this update

    def resize(self, top, nlines, ncols):
        'Assign, recalculate window dimensions'
        self.top = top # line number on display of first line of this window
        self.nlines = nlines # n of lines in window, excluding status line
        self.ncols = ncols # max number of chars in a line
        self.buf.npage = self.nlines #initial page size for ed z paging command

    def wline(self, iline):
        'Line number on display of iline in buffer.'
        return self.top + (iline - self.btop)

    def blast(self):
        'Index in buffer of last text line in the window, maybe not at bottom'
        return min(self.btop + self.nlines - 1, self.buf.S())
 
    def bottom(self):
        'Line number on display of bottom line in window (but not status line)'
        return self.top + self.nlines - 1

    def statusline(self):
         "Line number on display of window's status line"
         return self.bottom() + 1

    def near_top(self, iline):
        """
        Line number in buffer iline 
        is in top half of segment at beginning of buffer that fits in window.
        """
        return (iline <= self.nlines//2 or self.buf.S() <= self.nlines)

    def near_bottom(self, iline):
        """
        Line number in buffer iline 
        is in bottom half of segment at end of buffer that fits in window.
        """
        return (self.buf.S() - iline < self.nlines//2 and
                self.buf.S() >= self.nlines)
 
    def empty_line(self, iline):
        'True when line number iline in buffer is empty, or is just \n'
        return self.buf.lines[iline] in ('','\n')

    def contains(self, iline):
        'True when line number iline in buffer is contained in the window'
        return (self.btop <= iline <= self.blast())
        
    def ch0(self, iline):
        'First character in line iline in buffer, or space if line is empty'
        return ' ' if self.empty_line(iline) else self.buf.lines[iline][0]

    def set_marker(self, wiline, iline):
        'Set marker on display line number wiline which shows buf line iline'
        display.put_render(wiline, 1, self.ch0(iline), display.white_bg)

    def clear_marker(self, wiline, iline):
        'Clear marker from display line wiline which shows buffer line iline'
        display.put_render(wiline, 1, self.ch0(iline), display.clear)

    def scroll(self, nlines):
        """
        Move segment of buffer displayed in window by nlines (pos or neg),
        but leave dot unchanged so window contents appear to scroll.
        """
        self.btop = clip(self.btop + nlines, 1, self.buf.S())

    def shift(self, nlines):
        """
        Move segment of buffer displayed in window by nlines (pos or neg),
        and shift dot also so window contents appear the same.
        """
        self.scroll(nlines)
        self.saved_dot = clip(self.saved_dot + nlines, 1, self.buf.S())

    def locate_segment(self, iline):
        """
        Given line number in buffer iline, position window by
        assigning self.btop, index in buffer of top line in window.
        """
        if self.near_top(iline):
            self.btop = 1  
        elif self.near_bottom(iline):
            self.btop = self.buf.S() - (self.nlines - 1) # last page
        else: 
            self.btop = iline - self.nlines//2 # center iline in window

    def open_line(self, wiline):
        'Make line empty at line number wiline on display'
        #if self.top <= wiline <= self.top + self.nlines-1: # omit,let it crash
        display.put_cursor(wiline, 1)
        display.kill_whole_line()

    def clear_lines(self, first, last):
        """
        Clear consecutive consecutive lines from first through last in window.
        Cursor must be positioned at first line already.
        """
        for i in range(first,last+1): # unempty if reached end of buffer
            display.kill_whole_line()
            print()

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
        return i+1 # fewer than first:last+1 when at end of buffer

    def update_lines(self, first, iline, last=0):
        """
        Write lines in window starting at line numbered first on the display,
        to the bottom of the window, or to line numbered last if arg present.
        Lines come from self.buf starting at its line iline.
        """
        self.first = first if self.first == 0 else self.first # DIAGNOSTIC
        last = last if last else self.bottom()
        blastline = iline + (last - first) # blastline might exceed $ near eob
        display.put_cursor(first, 1)
        nprinted = self.render_lines(iline, blastline)
        icursor = first + nprinted
        self.nprinted += nprinted # DIAGNOSTIC
        self.clear_lines(icursor, last)
        
    def update_for_input(self):
        """
        Open next line and overwrite lines below.
        If at bottom of window, scroll insertion point up to the middle.
        Then place input cursor.
        """
        wdot = self.wline(self.buf.dot) # line on display where dot appears
        if wdot > 0:
            display.put_render(wdot, 1, self.buf.lines[self.buf.dot][0],
                               display.clear) # erase cursor at dot
        if wdot >= self.top + self.nlines - 1: # at bottom of window
            self.scroll(self.nlines//2)
            wdot = self.top + (self.buf.dot - self.btop)
            self.update_lines(self.top, self.buf.dot-self.nlines//2+1, 
                              last=wdot)
        self.open_line(wdot+1)
        self.update_lines(wdot+2, self.buf.dot+1)

    def render_status_prefix(self):
        "Print information about window's buffer in its status line."
        s1 = self.statusline()
        unsaved = '-----**-     ' if self.buf.unsaved else '--------     ' # 13
        bufname = '%-13s' % self.buf.name
        position = (' All ' if self.buf.S() <= self.nlines else # S() is last line
                    ' Top ' if self.btop == 1 else
                    ' Bot ' if self.blast() == self.buf.S() else
                    ' %2.0f%% ' % (100*self.buf.dot/(len(self.buf.lines)-1)))
        linenums = '%-14s' % ('L%d/%d ' % (self.buf.dot if self.current 
                                           else self.saved_dot, self.buf.S()))
        display.put_render(s1, 0, unsaved, display.white_bg)
        display.put_render(s1, 13, bufname, display.bold, display.white_bg)
        display.put_render(s1, 22, position, display.white_bg) # was 26
        display.put_render(s1, 27, linenums, display.white_bg) # was 31

    def render_status(self):
        "Print information about window's buffer in its status line."
        self.render_status_prefix()
        timestamp = datetime.strftime(datetime.now(),' %H:%M:%S -') # 10 char
        s1 = self.statusline()
        display.put_render(s1, 45, '-'*(self.ncols-(45+10)), display.white_bg)
        display.put_render(s1, self.ncols-10, timestamp, display.white_bg)

    def render_status_info(self, update):
        "Print diagnostic and debug information in the status line."
        self.render_status_prefix()
        s1 = self.statusline()
        Window.nupdates += 1 # ensure at least this changes in status line
        update_info = '%3d %3s o:%3d d:%3d s:%3d e:%3d, f:%3d n:%3d' % \
            (Window.nupdates, str(update.op)[3:6],
             update.origin, update.destination, update.start, update.end, 
             self.first, self.nprinted)
        display.put_render(s1, 36, update_info, display.white_bg) # was 40
        display.kill_line()
        self.first = 0    # reset after each update
        self.nprinted = 0 
