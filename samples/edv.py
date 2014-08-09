"""
edv - visual ui for ed. 

This is platform-dependent.  Requires display to use ansi control codes.
Probably requires Unix-like OS to get display geometry. Tested on mac terminal.
"""

# For now just call ed_cmd
# all input and output in a 3-line scrolling region at the bottom.

import sys
import traceback
import subprocess
import ed0, ed, ansi

# display geometry - works on Mac OS X, probably other Unix
nlines, ncolumns = [ int(n) 
                     for n in subprocess.check_output(['stty','size']).split()]

# position display elements
# count backwards (upwards) from the end (display bottom)
# elt1, eltn are display line numbers of first, last line in element
# line numbers on display are 1-based as in ansi and ed 

# scrolling command window at the bottom
# start with 3 lines: prev command, response to prev cmd, new command
hcmd = 2 # lines, show more to see ed command history
cmd1, cmdn = nlines-hcmd+1, nlines # +1 because nlines is last line

# buffer status with buffer name etc
hstatus = 1 # just one line
status1 = cmd1 - hstatus - 1

def display_status(line, bufname):
    'On given line, print information about named buffer.'
    # based on print_status in ed, but full window width
    buf = ed0.buffers[bufname]
    # later, maybe optimize by printing these fields separately
    loc = '%s/%d' % (buf.dot, len(buf.lines)-1) # don't count empty first line
    filename_str = buf.filename if buf.filename else 'no current filename'
    status = '%7s  %s%s%-12s  %s' % (loc, 
                               '.' if bufname == ed0.current else ' ',
                               '*' if buf.unsaved else ' ', 
                               bufname, filename_str)
    status += (ncolumns - (25 + len(filename_str)))*' ' # bg_color all ncolumns
    print ansi.cup % (line, 1) # cursor to buffer status line    
    ansi.render(status, ansi.white_bg) # actually gray on mac term

# text window - just one for now
win1, winn = 1, status1 - 1  # first and last line numbers
wlen = winn - win1 + 1  # number of lines
wtop = wlen/2 # number of lines in top half, python 2 integer division
wbot = wlen - wtop # number of lines in bottom half, maybe wtop+1

def display_centered(win1, wlen, bufname):
    """
    Start at line win1, display wlen lines from named buffer centered on dot
    Rewrites every line from win1 through win1 + wlen - 1
    """
    buf = ed0.buffers[bufname]
    # center dot in window
    itop = buf.dot - wtop # index of buffer line at top of window
    ibot = buf.dot + wbot - 1 #  " at bottom "
    # adjust itop, ibot if dot is too near top or bottom of buffer
    if itop < 1: # first valid buffer line is always index 1 not 0
        itop, ibot = 1, ibot + (1-itop)
    last = len(buf.lines)-1 # index of last line in buffer, same as ed0.S()
    if ibot > last:
        ibot = last
    # FIXME if dot is near last, this wastes space at window bottom
    wblank = wlen - (ibot-itop+1) # number of blank lines at bottom of window
    print ansi.cup % (win1,1),  # cursor to window top
    for line in buf.lines[itop:ibot+1]:
        print line.rstrip(), # remove trailing \n stored with line
        print ansi.el % 0 # erase to end of line, print \n to advance to next
    for line in range(wblank):
        print ansi.el % 2 # erase entire line, advance to next

def init_display():
    'Clear screen, update display'
    print ansi.cup % (1,1), # cursor to origin, don't advance to next line
    print ansi.ed # clear screen from cursor
    print ansi.decstbm % (cmd1, cmdn), # set scrolling region
    update_display()

def update_display():
    'Show windows, set scroll to command window, cursor to bottom'
    display_centered(win1, wlen, ed0.current) # FIXME? - rewrites everthing!
    display_status(status1, ed0.current)
    # use write not print, we don't want newline or trailing space
    sys.stdout.write(ansi.cup % (cmdn, 1)) # cursor to col 1, line at bottom

def restore_display():
    'restore full-screen scrolling, cursor to bottom'
    print(ansi.decstbmn)
    print(ansi.cup % (nlines,1))

def edv_cmd(cmd):
    'process one command without blocking'
    try:
        ed.ed_cmd(cmd) # non-blocking
        update_display()
    except BaseException as e:
        restore_display() # so we can see entire traceback 
        traceback.print_exc() # looks just like unhandled exception
        exit()

def edv():
    """
    Top level edv command to invoke from python prompt or command line
    Won't cooperate with Piety scheduler, calls blocking command raw_input
    """
    init_display()
    cmd = '' # anything but 'q', must replace 'q' from previous quit
    while not cmd == 'q':
        cmd = raw_input() # blocking. no prompt - maybe make prompt a parameter
        edv_cmd(cmd) # no blocking
    restore_display()

# Run the editor from the system command line: python edv.py
if __name__ == '__main__':
    edv()
