"""
edd - display editor based on the line editor ed.py.  

Described in ed.md etc.  To run: python3 edd.py or import edd then edd.main()
"""

import traceback, os
import terminal, display, window, ed

# suppress output from ed l z commands to scrolling command region
null = open(os.devnull, 'w')
ed.destination = null

# Position display elements.  For now, just two regions from top to bottom:
#  1. text buffer window including buffer status line(s)
#  2. scrolling command input region
# Line numbers on display and in each element are 1-based as in ed and ansi.

nlines, ncols = terminal.dimensions()

# Defaults, might be updated while program is running, especially cmd_h:

prompt = '' # command prompt

win_1 = 1 # line number on display of first line of first window
status_h = 1 # height (lines) of buffer status, now just a status line
             # for now this must be the same for all windows
cmd_h = 2  # height (lines) of scrolling command region at the bottom
cmd_1 = None # line num on display of 1st line of scrolling command region
cmd_n = None #  " bottom "
win_h = None # total number of lines in all windows (vertical stack)

win = None # assign window to this in init_display, below

# Values saved before ed command so we can test for changes after
(cmd_h0, current0, filename0, cursor_i0, cursor_ch0) = (None, None, None, 
                                                        None, None)

def save_parameters():
    'Save window parameters before ed cmd so we can test for changes after'
    global cmd_h0, current0, filename0, cursor_i0, cursor_ch0
    cmd_h0, current0, filename0, cursor_i0, cursor_ch0 = \
        cmd_h, ed.current, ed.buf.filename, win.cursor_i, win.cursor_ch

def print_saved():
    'for debug prints'
    print('cmd_h0 %s, current0 %s, filename0 %s, cursor_i0 %s, cursor_ch0 %s' %
          (cmd_h0, current0, filename0, cursor_i0, cursor_ch0))

def layout_changed():
    'Window dimensions or locations changed'
    return cmd_h != cmd_h0 # only one window for now

def file_changed():
    'Current buffer changed or different file loaded in current buffer'
    return ed.current != current0 or ed.buf.filename != filename0

def text_cmd():
    'Buffer text contents changed in buffer segment visible in window'
    return ed.cmd_name in 'aicds' # append, insert, change, delete, substitute

def calc_layout():
    'Calculate dimensions and location of window'
    # Currently there is only one window
    # scrolling command region at the bottom
    global cmd_1, cmd_n, win_h
    cmd_1 = nlines - cmd_h + 1 # first line after cmd_h lines
    cmd_n = nlines # bottom of display
    # text window element - just one window for now, may add others later
    win_h = nlines - cmd_h # fills remaining space

def set_command_cursor():
    'Put cursor at input line in scrolling command region'
    display.put_cursor(cmd_n, 1) # bottom line

def init_display(*filename, **options):
    """
    Clear and render entire display, set scrolling region, place cursor
    Process optional arguments: filename, options if present
    """
    global prompt, cmd_h, win
    if filename:
        ed.e(filename[0])
    if 'p' in options:
        prompt = options['p'] 
    if 'h' in options:
        cmd_h = options['h'] 
    calc_layout() # initialize cmd_1, cmd_n etc.
    display.put_cursor(1,1) # origin, upper left corner
    display.erase_display() 
    # Initially there is just one window displaying 'main' buffer
    win = window.Window(ed.buf, win_1, win_h, ncols) 
    win.update_window(ed.command_mode)
    display.set_scroll(cmd_1, cmd_n) 
    set_command_cursor()

def update_display():
    'Show window, cursor, status line. Set scroll to input region,place cursor'
    win.locate_cursor() # assign new cursor_i
    # recalculate layout and redisplay everything
    if layout_changed():
        init_display()
    # New contents or cursor outside window, redisplay window and cursor
    elif file_changed() or text_cmd() or win.cursor_elsewhere():
        win.update_window(ed.command_mode)
        # update_window manages in-window display cursor and input cursor
        if ed.command_mode:
            set_command_cursor() # scrolling-region cursor for command entry
    # Cursor remained in window, move cursor only
    elif win.cursor_moved(cursor_i0):
        win.erase_cursor(cursor_i0, cursor_ch0)
        win.display_cursor()
        win.display_status()
        set_command_cursor()
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
        if line == 'Z': # move cursor backward a page
            ed.cmd('-%dp' % ed.buf.npage) 
        elif line == ' ': # backward a line
            ed.cmd('-1p')
        # RET in ed already moves forward a line
        else:
            ed.cmd(line) # non-blocking
        if ed.cmd_name in 'bBeED':
            win.buf = ed.buf # ed.buf might have changed
        update_display()
    except BaseException as e:
        restore_display() # so we can see entire traceback 
        traceback.print_exc() # looks just like unhandled exception
        exit()

def main(*filename, **options):
    """
    Top level edd command to invoke from python prompt or command line.
    Won't cooperate with Piety scheduler, calls blocking command raw_input.
    """
    ed.quit = False # allow restart
    init_display(*filename, **options)
    while not ed.quit:
        line = input(prompt) # blocking
        cmd(line) # no blocking
    restore_display()

# Run the editor from the system command line: python edd.py
if __name__ == '__main__':
    main()
