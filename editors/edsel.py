"""
edsel - display editor based on the line editor ed.py.  

Described in ed.md and edsel.md.  To run: python3 edsel.py or import edsel then edsel.main()
"""

import traceback, os
import terminal, display, window, ed

prompt = '' # command prompt

# The frame is the entire region on the display occupied by the editor.
# On a typical host desktop, the frame occupies an entire terminal window.
# There are two main regions in the frame.  Top to bottom, they are:
#  1. One or more windows into text buffer(s)
#     In this version, windows are stacked vertically (not side by side).
#  2. scrolling command input region
# Line numbers on display and in each region are 1-based as in ed and ansi.

nlines, ncols = terminal.dimensions() # frame_h, frame_w = nlines, ncols

# Default frame dimensions, might be updated while running, especially cmd_h:
frame_top = 1 # line number on display of first line of frame
cmd_h = 2  # height (lines) of scrolling command region at the bottom

# These are assigned by calc_frame called from init_session and update_frame
windows_h = None # total number of lines in windows region of frame (all windows)
cmd_1 = None # line number on display of first line of scrolling command region
cmd_n = None #  " bottom "

# first window is assigned from init_session after cmd_h etc. are assigned
win_i = None # current window index
win = None # current window
windows = list() # list of windows, windows[win_i] is the current window

# Values saved before ed command so we can test for changes after, or use them
(cmd_h0, current0, filename0, win0) = (None, None, None, None)

# flags for update_display
set_other_window = False
set_single_window = False
split_window = False

def clear_flags():
    global set_other_window, set_single_window, split_window
    set_other_window, set_single_window, split_window = False, False, False

def save_parameters():
    'Save frame + window info before ed cmd so we can test for changes after'
    global cmd_h0, current0, filename0
    cmd_h0, current0, filename0 = cmd_h, ed.current, ed.buf.filename

def print_saved():
    'for debug prints'
    print('cmd_h0 %s, current0 %s, filename0' % (cmd_h0, current0, filename0))

def frame_changed():
    'Dimensions or locations of regions within frame changed'
    # We do not handle the frame size itself changing
    return cmd_h != cmd_h0

def file_changed():
    'Current buffer changed or different file loaded in current buffer'
    return ed.current != current0 or ed.buf.filename != filename0

def text_cmd():
    'Buffer text contents changed in buffer segment visible in window'
    return ed.cmd_name in 'aicdsymtr' # append, insert, change, delete, substitute, yank etc.

def calc_frame():
    'Calculate dimensions and location of window and scrolling command region'
    global cmd_1, cmd_n, windows_h
    cmd_1 = nlines - cmd_h + 1 # scrolling cmd region, index of first line
    cmd_n = nlines # last line on display
    windows_h = nlines - cmd_h # text window fills remaining space
    # frame_top, ncols unchanged

def set_command_cursor():
    'Put cursor at input line in scrolling command region'
    display.put_cursor(cmd_n, 1) # last line on display

def update_windows():
    'redraw all windows, called by display_frame, for example after frame resize'
    for w in windows:
        w.update_window(False) # no windows could be in insert mode at this time

def display_frame():
    'Clear and update the entire frame'
    # called from init_session and update_frame
    display.put_cursor(1,1) # origin, upper left corner
    display.erase_display() 
    update_windows()
    display.set_scroll(cmd_1, cmd_n) 
    set_command_cursor()

def update_frame():
    'Recalculate frame and all window dimensions, then display all.'
    # Makes all windows (almost) the same height, unlike after o2 command
    calc_frame() # recalculate global cmd_1 cmd_n windows_h
    nwindows = len(windows)
    win_h0 = windows_h // nwindows # integer division
    for iwin, win in enumerate(windows):
        win_h = win_h0 if iwin < nwindows-1 else windows_h - (nwindows-1)*win_h0
        win.resize(frame_top + iwin*win_h0, win_h, ncols)
    display_frame()

def init_session(*filename, **options):
    """
    Clear and render entire display, set scrolling region, place cursor.
    Process optional arguments: filename, options if present.
    """
    global prompt, cmd_h, win, win_i
    if filename:
        ed.e(filename[0])
    if 'p' in options:
        prompt = options['p'] 
    if 'h' in options:
        cmd_h = options['h'] 
    ed.discard_printing() # suppress ed output to scrolling command region
    # must calc_frame to get window dimensions before we create win
    calc_frame() # assign windows_h etc.
    win = window.Window(ed.buf, frame_top, windows_h, ncols) # one big window
    windows.append(win) 
    win_i = 0 # Now win == windows[win_i]
    display_frame()


def update_display():
    """
    Check for any needed display updates.  If there are any, do them'
    All the display update case analysis is in this function.  
    """
    cursor_at_command  = True
    if frame_changed(): # update all windows and cursor
        update_frame()  # calls display_frame, which calls update_windows
        return
    win.locate_cursor() # assign new cursor_i
    if set_other_window:
        # move cursor to new current window, don't update window content
        win0.locate_cursor()
        win0.erase_cursor()
        win.display_cursor()
        cursor_at_command = False
    elif (file_changed() or text_cmd() or win.cursor_elsewhere() 
        or set_single_window or split_window):
        # update current window contents and cursor
        win.update_window(not ed.command_mode) # insert mode
        if ed.command_mode:
            win.display_cursor() # dot cursor in window
        if split_window: 
        #  win0 is former current window, delete cursor then update
            win0.locate_cursor()
            win0.erase_cursor()
            win0.update_window(not ed.command_mode)
        cursor_at_command = False
    elif win.cursor_moved():
        # update cursor only in current window, don't update window content
        win.erase_cursor()
        win.display_cursor()
        win.display_status()
        cursor_at_command = False
    # FIXME: more cases - contents change in window other than the current window
    #  can happen when multiple windows view the same buffer
    else: 
        # some commands do not affect windows: A b (with no args) f k n w 
        pass
    if ed.command_mode and not cursor_at_command:
        set_command_cursor()

def restore_display():
    'Restore full-screen scrolling, cursor to bottom.'
    display.set_scroll_all()
    display.put_cursor(nlines,1)

def o(line):
    """
    Window commands - these are not ed commands, they are handled here.
    For now there is just one vertical stack of windows in the frame.
    """
    global win, win_i, win0, \
        set_other_window, set_single_window, split_window
    param_string = line.lstrip()[1:].lstrip()
    # o: switch to next window
    if not param_string:
        win_i = win_i+1 if win_i+1 < len(windows) else 0
        win0 = win
        win = windows[win_i] 
        ed.b(win.buf.name) # change current buffer
        set_other_window = True
        return
    else:
        try:
            param = int(param_string)
            # o1: return to single window
            if param == 1:
                # delete all but current window
                del windows[:win_i]   
                del windows[win_i+1:]
                win_i = 0
                win = windows[win_i]
                win.resize(frame_top, windows_h, ncols) # one big window
                set_single_window = True
                return
        # o2: split window, horizontal
            elif param == 2:
                # put the new window at the top
                new_win_h = win.win_h // 2 # integer division
                win.resize(frame_top + new_win_h, win.win_h - new_win_h, ncols) # old window
                win0 = win
                win = window.Window(ed.buf, frame_top, new_win_h, ncols) # new window
                windows.insert(win_i, win)
                win = windows[win_i] # no need to adjust win_i after insert
                split_window = True
                return
            # maybe more options later
            else:
                return
        except ValueError:
            print('? integer expected at %s' % param_string)
            return 

def cmd(line):
    'Process one command line without blocking.'
    # try/except ensures we restore display, especially scrolling
    try:
        save_parameters() # before ed.cmd
        # intercept special commands used by edsel only, not ed
        if line.lstrip().startswith('o'):
            o(line) # window commands
        else:
            ed.cmd(line) # non-blocking
            if ed.cmd_name in 'bBeED':
                win.buf = ed.buf # ed.buf might have changed
        update_display() # contains all update logic, may do nothing
        clear_flags() # flags used by update_display, maybe set above
    except BaseException as e:
        restore_display() # so we can see entire traceback 
        traceback.print_exc() # looks just like unhandled exception
        exit()

def main(*filename, **options):
    """
    Top level edsel command to invoke from python prompt or command line.
    Won't cooperate with Piety scheduler, calls blocking command raw_input.
    """
    ed.quit = False # allow restart
    init_session(*filename, **options)
    while not ed.quit:
        line = input(prompt) # blocking
        cmd(line) # no blocking
    restore_display()

# Run the editor from the system command line: python edsel.py
if __name__ == '__main__':
    main()
