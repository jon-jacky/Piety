"""
edv - ed viewer.  Display ed buffer contents around dot in window.
      
Update window contents as ed commands move dot or change buffer contents.
Not really a display editor, but maybe more convenient than bare ed.

Platform-dependent.  Requires display to use ansi control codes.
Probably requires Unix-like OS to get display geometry. Tested on mac terminal.
"""

import sys
import traceback
import subprocess
import ed0, ed, ansi

render = sys.stdout.write # unlike print, don't write newline or space

# Get display dimensions.  This works on Mac OS X, probably other Unix.
nlines, ncols = [ int(n) 
                  for n in subprocess.check_output(['stty','size']).split()]

# Position display elements.  For now, just three regions from top to bottom:
#  1 text buffer window  2 buffer status line  3 scrolling command input region
# Line numbers on display and in each element are 1-based as in ed and ansi.

# Defaults, might be updated while program is running, especially cmd_h:

win_1 = 1 # line number on display of first line of buffer text window
status_h = 1 # height (lines) of buffer status, now just a status line
cmd_h = 2  # height (lines) of scrolling command region at the bottom

# The following depend on the preceding, are all updated by functions below:

win_h = None # number of lines in text buffer window
win_n = None # line number on display of last line in buffer text window

status_1 = None # line number on display of first line of buffer status region

cmd_1 = None # line number on display of first line of scrolling command region
cmd_n = None #  " bottom "

seg_1 = None # index in buffer of first line displayed in text window
seg_n = None #  " last "

cursor_i = None # line number of dot on display, if it is visible, else 0

# Values saved before ed command so we can test for changes after
cmd_h0, current0, filename0, cursor_i0 = None, None, None, None

def save_parameters():
    'Store window parameters before ed cmd so we can test for changes after'
    global cmd_h0, current0, filename0, cursor_i0
    cmd_h0, current0, filename0, cursor_i0 = \
        cmd_h, ed0.current, ed.buf().filename, cursor_i

def layout_changed():
    return cmd_h != cmd_h0

def contents_changed():
    return ed0.current != current0 or ed.buf().filename != filename0

def calc_layout():
    """
    Calculate window dimensions and positions
    """
    global cmd_1, cmd_n, status_1, win_h, win_n, seg_1, seg_n
    # scrolling command region at the bottom
    cmd_1 = nlines - cmd_h + 1 # +1 because nlines is last within cmd element
    cmd_n = nlines # bottom of display
    # status line below text window
    status_1 = cmd_1 - status_h # no +1, cmd_1 is first after status element
    # text window element - just one window for now, may add others later
    win_h = nlines - (cmd_h + status_h) # fills remaining space
    win_n = win_1 + win_h - 1 # last before status, should equal status_1-1  
    # seg_1, seg_n are indices in buffer of first, last lines shown in window
    seg_1 = 1 
    seg_n = min(win_h, ed.S())

def display_status(status_1, bufname):
    'Starting on status_1 line, print information about named buffer.'
    # based on print_status in ed, but full window width
    buf = ed0.buffers[bufname] # ed.buf() is ed0.buffers[current] not ...[bufname]
    # later, maybe optimize by printing these fields separately
    loc = '%s/%d' % (buf.dot, len(buf.lines)-1) # don't count empty first line
    filename_str = buf.filename if buf.filename else 'no current filename'
    status = '%7s  %s%s%-12s  %s' % (loc, 
                               '.' if bufname == ed0.current else ' ',
                               '*' if buf.unsaved else ' ', 
                               bufname, filename_str)
    status += (ncols - (25 + len(filename_str)))*' ' # bg_color all ncols
    render(ansi.cup % (status_1, 1)) # cursor to buffer status line    
    ansi.render(status, ansi.white_bg) # white_bg is actually gray on mac term

def locate_window(bufname):
    """
    Compute segment of buffer that is visible in window
    Assign seg_1, seg_n: indices in buffer of first, last lines shown in window
    Center window on dot if possible, otherwise show top or bottom of buffer
    """
    global seg_1, seg_n
    buf = ed0.buffers[bufname] # ed.buf() is ed0.buffers[current] not ...[bufname]
    # Visible segment is at top of buffer, begins at first line
    if ed.o() < win_h/2 or ed.S() <= win_h: # win_h/2 python 2 integer division
        seg_1 = 1  
        seg_n = min(win_h, ed.S())
    # Visible segment is at bottom of buffer, ends at last line
    elif ed.S() - ed.o() < win_h/2 and ed.S() >= win_h: 
        seg_1 = ed.S() - (win_h - 1)
        seg_n = ed.S()
    # Visible segment is centered on dot
    else:
        seg_1 = ed.o() - win_h/2  
        seg_n = seg_1 + (win_h - 1)

def display_window(bufname):
    """
    Start on win_1 line, display lines seg_1 .. seg_n from buffer bufname 
    If space remains in window, pad with empty lines to win_h
    """
    buf = ed0.buffers[bufname] # ed.buf() is ed0.buffers[current] 
    seg_h = seg_n - seg_1 + 1 # lines in segment, usually same as win_h
    blank_h = win_h - seg_h   # n of padding empty lines at window bottom
    render(ansi.cup % (win_1,1))  # cursor to window top
    for line in buf.lines[seg_1:seg_n+1]: # python slice, upper limit excluded
        print line.rstrip()[:ncols-1], # remove trailing \n, truncate don't wrap
        print ansi.el_end    # erase to end of line, print \n to advance to next
    for line in range(blank_h):
        print ansi.el_all # erase entire line, advance to next

def locate_cursor(bufname):
    """
    Update cursor_i, line number of dot on display, if it is visible, else 0
    """
    global cursor_i
    buf = ed0.buffers[bufname] # ed.buf() is ed0.buffers[current] 
    if ed0.S(): # buffer not empty
        cursor_i = win_1 + (buf.dot - seg_1)
        cursor_i = cursor_i if win_1 <= cursor_i <= win_1 + win_h - 1 else 0
    else:
        cursor_i = 0 # , cursor_c, cursor_g = 0, '', ''

def remove_cursor(cursor_i, ch):
    'At start of line cursor_i, replace cursor with character ch, no attributes'
    render(ansi.cup % (cursor_i, 1))
    ansi.render(ch, ansi.clear_all)

def display_cursor(cursor_i, ch):
    'At start of line cursor_i, put character ch with attributes'
    render(ansi.cup % (cursor_i, 1))
    ansi.render(ch, ansi.white_bg) # no blink_slow, too noisy

def init_display():
    'Clear screen, render display.'
    bufname = ed0.current
    buf = ed0.buffers[bufname] # ed.buf() is ed0.buffers[current] not ...[bufname]
    # layout
    calc_layout() # initialize cmd_1, cmd_n etc.
    render(ansi.cup % (1,1)) # cursor to origin, don't advance to next line
    render(ansi.ed) # clear screen from cursor
    # window
    locate_window(bufname) # assign seg_1, seg_n
    display_window(bufname)
    # cursor
    locate_cursor(bufname) # assign cursor_i
    if cursor_i:
        chx = buf.lines[buf.dot][0] # first char on line, makes blinking cursor
        chx = '_' if chx in (' ','\n') else chx # make space or empty visible
        display_cursor(cursor_i, chx)
    # scrolling input region
    render(ansi.decstbm % (cmd_1, cmd_n)) # set scrolling region

def update_display():
    'Show window, cursor, status line, set scroll to input region, place cursor'
    bufname = ed0.current
    if True: # FIXME layout_changed() or contents_changed():
        init_display()
    elif False: # FIXME cursor moved outside already displayed window
        pass
    else: # FIXME cursor remained in window
        pass
    display_status(status_1, bufname)
    render(ansi.cup % (cmd_n, 1)) # cursor to col 1, line at bottom

def restore_display():
    'Restore full-screen scrolling, cursor to bottom.'
    print(ansi.decstbmn)
    print(ansi.cup % (nlines,1))

def edv_cmd(cmd):
    'Process one command without blocking.'
    try:
        # special cases, command synonyms
        if cmd == 'Z': # move cursor forward a page
            ed.ed_cmd('+%dp' % ed.buf().npage) 
        elif cmd == 'X': # backward a page
            ed.ed_cmd('-%dp' % ed.buf().npage) 
        elif cmd == ' ': # backward a line
            ed.ed_cmd('-1p')
        # RET in ed already moves forward a line
        else:
            ed.ed_cmd(cmd) # non-blocking
        update_display()
    except BaseException as e:
        restore_display() # so we can see entire traceback 
        traceback.print_exc() # looks just like unhandled exception
        exit()

def edv(scroll_h=cmd_h):
    """
    Top level edv command to invoke from python prompt or command line.
    Won't cooperate with Piety scheduler, calls blocking command raw_input.
    scroll_h sets n of lines in bottom scrolling region, defaults to cmd_h
    """
    cmd_h = scroll_h
    init_display()
    display_status(status_1, ed0.current)
    render(ansi.cup % (cmd_n, 1)) # cursor to col 1, line at bottom
    cmd = '' # anything but 'q', must replace 'q' from previous quit
    while not cmd == 'q':
        cmd = raw_input() # blocking. no prompt - maybe make prompt a parameter
        edv_cmd(cmd) # no blocking
    restore_display()

# Run the editor from the system command line: python edv.py
if __name__ == '__main__':
    edv()
