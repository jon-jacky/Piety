"""
edv - visual ui for ed. 

This is a platform-dependent module.  Requires display uses ansi control codes,
Probably requires Unix-like OS to get display geometry. Tested on mac terminal.
"""

# For now just call ed_cmd
# all input and output in a 3-line scrolling region at the bottom.

import traceback
import subprocess
import ed0, ed, ansi

# display geometry - works on Mac OS X, probably other Unix
nlines, ncolumns = subprocess.check_output(['stty', 'size']).split()
nlines = int(nlines)
ncolumns = int(ncolumns)

# position display elements
# count backwards (upwards) from the end (display bottom)
# elt1, eltn are display line numbers of first, last line in element
# line numbers on display are 1-based as in ansi and ed 

# scrolling command window at the bottom
# minimum 3 lines: prev command, response to prev cmd, new command
hcmd = 3 # lines
cmd1, cmdn = nlines-hcmd+1, nlines # +1 because nlines is last line

# buffer status with buffer name etc
hstatus = 1 # just one line
status1 = cmd1 - hstatus - 1
    
def print_status(line, bufname):
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

def init_display():
    'clear screen, show windows, set scroll to command window, cursor to bottom'
    print ansi.cup % (1,1), # cursor to origin, don't advance to next line
    print ansi.ed # clear screen from cursor
    print_status(status1, ed0.current)
    print ansi.decstbm % (cmd1, cmdn) # set scrolling region
    print ansi.cup % (cmdn, 1) # cursor to bottom

def restore_display():
    'restore full-screen scrolling, cursor to bottom'
    print(ansi.decstbmn)
    print(ansi.cup % (nlines,1))

def edv_cmd(cmd):
    'process one command without blocking'
    try:
        ed.ed_cmd(cmd) # non-blocking
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
