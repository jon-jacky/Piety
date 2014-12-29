"""
edd - display editor based on the line editor ed.py.  
  Described in ed.md.  To run: python edd.py or import edd then edd.main()
"""

import traceback
import subprocess # just to get display dimensions
import ansi_display as display
import ed

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

cursor_i = None # line number of current buffer dot on display
cursor_ch = None # character that cursor overwrites
cursor_chx = None # cursor character, same as cursor_ch except when it's blank

# Values saved before ed command so we can test for changes after
cmd_h0, current0, filename0, cursor_i0, cursor_ch0 = None, None, None, None, None

def save_parameters():
    'Save window parameters before ed cmd so we can test for changes after'
    global cmd_h0, bufname0, filename0, cursor_i0, cursor_ch0
    cmd_h0, bufname0, filename0, cursor_i0, cursor_ch0 = \
        cmd_h, ed.bufname(), ed.buf().filename, cursor_i, cursor_ch

def layout_changed():
    'Window dimensions or locations changed'
    return cmd_h != cmd_h0 # only one window for now

def file_changed():
    'Current buffer changed or different file loaded in current buffer'
    return ed.bufname() != bufname0 or ed.buf().filename != filename0

def text_changed():
    'Buffer text contents changed in buffer segment visible in window'
    return ed.cmd_name in 'aicds' # append, insert, change, delete, substitute
    
def cursor_moved():
    'Cursor moved to a different line on the display'
    return cursor_i != cursor_i0

def cursor_elsewhere():
    'Cursor lies outside segment of buffer visible in window'
    # buf() is okay here, this can only be called on current buffer
    dot_i = ed.buf().dot # line number of cursor in buffer (not screen)
    return (not seg_1 <= dot_i <= seg_n) if dot_i else False

def calc_layout():
    'Calculate window dimensions and locations'
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
    seg_n = min(win_h, ed.S()) # FIXME? ed.S() is for current buffer
    # adjust page size used with z Z X commands
    ed.buf().npage = win_h - 1

# Following functions take bufname arg, might be extended to multiple windows

def display_status(bufname):
    'Starting on status_1 line, print information about named buffer.'
    # based on print_status in ed, but full window width
    buf = ed.buffer(bufname)
    # later, maybe optimize by printing these fields separately
    loc = '%s/%d' % (buf.dot, len(buf.lines)-1) # don't count empty first line
    filename_str = buf.filename if buf.filename else 'no current filename'
    status = '%7s  %s%s%-12s  %s' % (loc, 
                               '.' if bufname == ed.bufname() else ' ',
                               '*' if buf.unsaved else ' ', 
                               bufname, filename_str)
    status += (ncols - (25 + len(filename_str)))*' ' # bg_color all ncols
    display.put_cursor(status_1, 1)
    display.render(status, display.white_bg) # white_bg is actually gray on mac term

def locate_window(bufname):
    """
    Compute segment of buffer that is visible in window
    Assign seg_1, seg_n: indices in buffer of first, last lines shown in window
    Center window on dot if possible, otherwise show top or bottom of buffer
    """
    global seg_1, seg_n
    buf = ed.buffer(bufname)
    buf_S = len(buf.lines)-1
    # Visible segment is at top of buffer, begins at first line
    if buf.dot < win_h/2 or buf_S <= win_h: # win_h/2 python 2 integer division
        seg_1 = 1  
        seg_n = min(win_h, buf_S)
    # Visible segment is at bottom of buffer, ends at last line
    elif buf_S - buf.dot < win_h/2 and buf_S >= win_h: 
        seg_1 = buf_S - (win_h - 1)
        seg_n = buf_S
    # Visible segment is centered on dot
    else:
        seg_1 = buf.dot - win_h/2  
        seg_n = seg_1 + (win_h - 1)

def display_lines(buf, first, last):
    'Display lines in buf numbered first through last '
    for line in buf.lines[first:last+1]: # slice, upper limit excluded
        print line.rstrip()[:ncols-1], # remove \n, truncate don't wrap
        display.kill_line() # erase from cursor to end
        print # advance to next line
    
def display_window(bufname):
    """
    Start on win_1 line, display lines seg_1 .. seg_n from buffer bufname 
    If space remains in window, pad with empty lines to win_h
    If in input mode, open line where text will be typed
    """
    buf = ed.buffer(bufname)
    seg_h = seg_n - seg_1 + 1 # lines in segment, usually same as win_h
    blank_h = win_h - seg_h   # n of padding empty lines at window bottom
    display.put_cursor(win_1,1)  # cursor to window top
    if ed.command_mode:
        display_lines(buf, seg_1, seg_n)
    else: # input mode and this window displays current buffer around dot
        display_lines(buf, seg_1, ed.o())
        display.kill_whole_line() # open line for input
        print # next line
        display_lines(buf, ed.o()+1, seg_n-1)
    for line in range(blank_h if ed.command_mode else blank_h - 1):
        display.kill_whole_line()
        print

def locate_cursor(bufname):
    """
    Update cursor_i, line number of dot on display, if it is visible, else 0
    Also update cursor_ch, the cursor character - we need to erase it later
    """
    global cursor_i, cursor_ch, cursor_chx
    buf = ed.buffer(bufname)
    if len(buf.lines)-1: # buffer not empty, don't count empty first line at index 0
        # cursor_ch is character at start of line that cursor overwrites
        cursor_ch = buf.lines[buf.dot][0]
        # To ensure cursor on space or empty line is visible, use cursor_chx
        cursor_chx = '_' if cursor_ch in (' ','\n') else cursor_ch
        cursor_i = win_1 + (buf.dot - seg_1)
        cursor_i = cursor_i if win_1 <= cursor_i <= win_1 + win_h - 1 else 0
    else:
        cursor_i = 0
        cursor_ch = ''

def display_cursor():
    'Display cursor at start of line cursor_i'
    if cursor_i:
        display.put_cursor(cursor_i, 1)
        display.render(cursor_chx, display.white_bg) # but no blink - that's too noisy

def erase_cursor():
    'At start of line cursor_i0, replace cursor with saved char, no attributes'
    if cursor_i0:
        # if line is empty must use ' ' to overwrite '_'
        ch = cursor_ch0 if not cursor_ch0 == '\n' else ' '
        display.put_cursor(cursor_i0, 1)
        display.render(ch, display.clear)

def update_window(bufname):
    'Locate and render one window and its cursor, also status line'
    locate_window(bufname) # assign new seg_1, seg_n
    locate_cursor(bufname) # *re*assign new cursor_i, cursor_ch
    display_window(bufname)
    if ed.command_mode: # and window shows current buffer around dot
        display_cursor()
    # else input mode, update_display will put cursor at open input line
    display_status(bufname)

def init_display():
    'Clear and render entire display, set scrolling region, place cursor'
    calc_layout() # initialize cmd_1, cmd_n etc.
    display.put_cursor(1,1) # origin, upper left corner
    display.erase_display() 
    update_window(ed.bufname())
    display.set_scroll(cmd_1, cmd_n) 
    display.put_cursor(cmd_n, 1) # bottom line

def update_display():
    'Show window, cursor, status line.  Set scroll to input region, place cursor'
    locate_cursor(ed.bufname()) # assign new cursor_i, cursor_ch
    # recalculate layout and redisplay everything
    if layout_changed():
        init_display()
    # New contents or cursor outside window, redisplay window and cursor
    elif file_changed() or text_changed() or cursor_elsewhere():
        update_window(ed.bufname())
        if ed.command_mode:
            display.put_cursor(cmd_n, 1) # line at bottom
        else: # input mode and window shows current buffer around dot
            display.put_cursor(cursor_i+1, 1) # open line after dot
    # Cursor remained in window, move cursor only
    elif cursor_moved():
        erase_cursor()
        display_cursor()
        display_status(ed.bufname()) # FIXME? could write line number only
        display.put_cursor(cmd_n, 1)
    else:
        pass # no changes to display

def restore_display():
    'Restore full-screen scrolling, cursor to bottom.'
    display.set_scroll_all()
    display.put_cursor(nlines,1)

def cmd(line):
    'Process one command line without blocking.'
    # try/except ensures we restore display, especially scrolling
    try:
        save_parameters() # before ed.cmd
        # special cases, command synonyms
        if line == 'Z': # move cursor forward a page
            ed.cmd('+%dp' % ed.buf().npage) 
        elif line == 'X': # backward a page
            ed.cmd('-%dp' % ed.buf().npage) 
        elif line == ' ': # backward a line
            ed.cmd('-1p')
        # RET in ed already moves forward a line
        else:
            ed.cmd(line) # non-blocking
        update_display()
    except BaseException as e:
        restore_display() # so we can see entire traceback 
        traceback.print_exc() # looks just like unhandled exception
        exit()

line = None # This must be global so text_changed() can test it

def main(scroll_h=cmd_h):
    """
    Top level edd command to invoke from python prompt or command line.
    Won't cooperate with Piety scheduler, calls blocking command raw_input.
    scroll_h arg sets n of lines in bottom scrolling region, defaults to cmd_h
    """
    global line, cmd_h
    cmd_h = scroll_h
    init_display()
    line = '' # anything but 'q', must replace 'q' from previous quit
    ed.quit = False # allow restart
    while not ed.quit:
        line = raw_input() # blocking. no prompt - make prompt a parameter?
        cmd(line) # no blocking
    restore_display()

# Run the editor from the system command line: python edd.py
if __name__ == '__main__':
    main()
