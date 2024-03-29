"""
frame.py - Multiwindow display implemented by a list of window instances,
            with a scrolling command region at the bottom of the display.
"""

from enum import Enum
import util, terminal, terminal_util, display, window

# console instance, if present, stores column where cursor should go
console = None # code below defaults to column 1 if no Console

class Mode(Enum):
    """
    Mode.command when executing commands typed on the command line.
    Mode.input or Mode.display when entering/editing text in a display window.
    """
    command = 1 # ed command mode
    input = 2   # ed input mode for a,i,c commmands
    display = 3 # edsel display mode

mode = Mode.command

# Data structures

nlines, ncols = terminal_util.dimensions()

# Default frame dimensions, might be updated while running, especially cmd_h:
frame_top = 1 # line number on display of first line of frame
cmd_h = None  # assign from application's startup only if not already assigned

# Assigned by scale()
windows_h = None # total number of lines of all windows, including status lines
cmd_1 = None # line number on display of first line of scrolling command region
cmd_n = None #  " bottom "

# First window is assigned from startup after cmd_h etc. are assigned
ifocus = None # index of window with input focus
win = None # window with input focus
windows = list() # list of windows, windows[ifocus] has input focus

# Helper functions, used within this module but not called by clients

def scale(nlines, cmd_h):
    """
    Calculate dimensions and location of windows and scrolling command region.'
    nlines - total number of lines on display
    cmd_h - number of lines in scrolling command region
    Update global cmd_1, cmd_n top and bottom of scrolling command region
    Update global windows_h combined height of all windows, the entire frame
    """
    global cmd_1, cmd_n, windows_h
    cmd_1 = nlines - cmd_h + 1 # scrolling command region, index of first line
    cmd_n = nlines # scrolling command region, last line
    windows_h = nlines - cmd_h # windows with status lines fill remaining space

def refresh_windows():
    'Refresh all windows, called by frame refresh, for example after resize.'
    for w in windows:
        w.refresh()

# Functions called by clients

def put_command_cursor():
    'Put cursor at command line in scroll region'
    display.put_cursor(cmd_n, 1) # last line on display
    if console: console.move_to_point() # set column, default 1

def put_display_cursor():
    'Put cursor at dot, point in focus window'
    wdot = win.wline(win.buf.dot)
    display.put_cursor(wdot, 1)
    if console: console.move_to_point() # set column, default 1

def put_message(msg):
    'While in display mode, write a message in scrolling command region'
    put_command_cursor()
    util.putstr(msg + '\n')
    put_display_cursor()

def init(cmd_h, buf):
    'Initialize frame with one window into buffer.'
    global win, ifocus
    # must assign frame size before create first window
    scale(nlines, cmd_h)
    win = window.Window(buf, frame_top, windows_h-1, ncols) # -1 excl status
    win.focus = True
    windows.append(win)
    ifocus = 0

# Select the mode

def input_mode():
    'Switch to ed input mode, for ed a i c commands.'
    global mode
    mode = Mode.input
    win.update_for_input()
    wdot = win.wline(win.buf.dot)
    display.put_cursor(wdot+1,1) # +1 so we can't use put_display_cursor

def command_mode():
    'Switch to ed command mode, ed . while in input mode.'
    global mode
    mode = Mode.command
    # Overwrite '.' line on display, and lines below.
    win.render_from(win.buf.dot + 1)
    win.set_marker(win.buf.dot)
    put_command_cursor()

def display_mode():
    'Switch to edsel display mode'
    global mode
    mode = Mode.display
    win.clear_marker(win.buf.dot)
    put_display_cursor()

# Manage the entire frame

def refresh():
    """
    Clear, update entire display in command mode, otherwise just the windows.
    """
    if mode == Mode.command:
        display.put_cursor(1,1)
        display.erase()
    refresh_windows()
    if mode == Mode.command:
        display.set_scroll(cmd_1, cmd_n)
        put_command_cursor()
    elif mode == Mode.display:
        put_display_cursor()

def rescale(new_cmd_h):
    """
    Recalculate frame and all window dimensions, then display all.
    new_cmd_h - new n of lines in scrolling cmd region, None for no change.
    """
    # Makes all windows (almost) the same height, unlike after o2 command
    global cmd_h
    cmd_h = new_cmd_h if new_cmd_h else cmd_h
    scale(nlines, cmd_h)
    nwindows = len(windows)
    win_hdiv = windows_h // nwindows
    for iwin, w in enumerate(windows):
        win_h = (win_hdiv if iwin < nwindows-1
                 else windows_h - (nwindows-1)*win_hdiv) # including status
        w.resize(frame_top + iwin*win_hdiv, win_h-1, ncols) # -1 excl status
        w.locate(w.buf.dot if w is win else w.saved_dot)
    refresh()

def restore():
    """
    Exit from the whole frame and all its windows.
    Restore normal terminal behavior: full screen scrolling, cursor at bottom.
    """
    display.set_scroll_all()
    display.put_cursor(nlines,1)

# Manage windows

def next():
    'Switch input focus to next window, edda o command'
    global ifocus, win
    w0 = win
    w0.focus = False
    w0.saved_dot = w0.buf.dot
    if mode == Mode.command: # next is available in display mode with ^o
        w0.clear_marker(w0.saved_dot)
    w0.update_status()
    ifocus = ifocus+1 if ifocus+1 < len(windows) else 0
    win = windows[ifocus]
    win.focus = True
    win.buf.dot = win.saved_dot
    win.update_status()
    if mode == Mode.command: # next is available in display mode with ^o
        win.set_marker(win.buf.dot)
        put_command_cursor()
    return win

def single():
    'Delete all but focus window, edda o1 cmd'
    global ifocus
    windows[:] = [win]
    ifocus = 0
    win.resize(frame_top, windows_h-1, ncols) # one window, -1 excl status
    win.update()
    if mode == Mode.command:
        win.set_marker(win.buf.dot) # single is only available in command mode
        put_command_cursor()

def hsplit():
    'Split window, new window above becomes focus window, edda o2 command'
    global win
    win_top = win.top
    win_nlines = win.nlines // 2
    w0 = win
    w0.focus = False
    w0.saved_dot = w0.buf.dot
    if mode == Mode.command:
        w0.clear_marker(w0.saved_dot)
    w0.resize(win_top + win_nlines, w0.nlines - win_nlines, ncols)
    w0.update()
    win = window.Window(win.buf,win_top,win_nlines-1,ncols) #-1 excl status
    win.focus = True
    windows.insert(ifocus, win)
    win.update()
    if mode == Mode.command:
        win.set_marker(win.buf.dot) # hsplit is only available in command mode
        put_command_cursor()

# Select the buffer displayed in the focus window, that has input focus

def create(buf):
    'Create new buffer in focus window, ed b B.'
    win.buf = buf
    win.saved_dot = win.buf.dot
    win.update()
    if mode == Mode.command:
        put_command_cursor()

def select(buf):
    'Change buffer in focus window, ed b E D.'
    win.buf = buf
    win.update()
    if mode == Mode.command:
        win.set_marker(win.buf.dot)
        put_command_cursor()

def remove(delbuf, buf):
    """
    Delete current buffer, ed D.
    delbuf is the deleted buffer, buf is the new current buffer.
    """
    for w in windows:
        if w.buf == delbuf:
            w.buf = buf
            w.update()
    if mode == Mode.command:
        win.set_marker(win.buf.dot)
        put_command_cursor()

# Update one or more windows with buffer contents, where the buffer 
# is implicit: it is the buffer displayed in the focus window.

def locate(origin, destination):
    """
    Move dot from origin to destinaton, ed cmd with address only
    """
    if win.contains(destination):
        win.update_status()
    else:
        win.update()
    if mode == Mode.command:
        if win.contains(destination):
            win.clear_marker(origin)
            win.set_marker(destination)
        put_command_cursor()

def insert(buf, start, end):
    """
    Insert text: ed a i c m r t y commands
    buf - buffer where text is inserted
    start, end - line numbers of inserted text after insertion
    """
    if buf == win.buf: # if buffer is the current buffer ...
        if mode != Mode.input: # ed commands m r t y
            win.modify(start, end)
        elif mode == Mode.input: # input mode after ed commands a i c
            win.update_for_input()
        for w in windows:
            if w.samebuf(win):
                w.adjust_insert(start, end)

    # Insert text into buffer buf when it is *not* the the current buffer.
    # Search for windows (if any) which display that buffer,
    # start, end - line numbers of inserted text after insertion.
    else: # ... else buf arg is not the current buffer ...
        for w in windows:
            if w.buf == buf:  
                w.saved_dot = w.buf.dot
                w.modify(start, end)

    # Now put the cursor back in focus window, or at command line
    if mode == Mode.input: # can't put input cursor til other windows done
        win.put_cursor_for_input()
    elif mode == Mode.display:
        put_display_cursor()
    elif mode == Mode.command:
        put_command_cursor()

def delete(start, end):
    """
    Delete text: ed d m command
    start, end - line numbers of deleted text before deletion
    Deleted lines were above win.buf.dot
    win.buf.dot may differ from start if we delete end of buffer
    See buffer d() method
    """
    win.modify(win.buf.dot, win.buf.dot)
    for w in windows:
        if w.samebuf(win):
            w.adjust_delete(start, end, win.buf.dot)
    if mode == Mode.command:
        win.set_marker(win.buf.dot)
        put_command_cursor()

def mutate(start, end):
    """
    Change text: ed s command
    start - first line in selection where substitutions made
    end - last line where substitution actually made
    Update all lines in start..end, don't know which lines changed
    """
    if mode == Mode.command and win.contains(start):
        win.clear_marker(start)
    win.mutate(start, end)
    if mode == Mode.command and win.contains(end):
        win.set_marker(end)
    for w in windows:
        if w.samebuf(win):
            if w.intersects(start, end):
                w.mutate_lines(start, end)
    if mode == Mode.command:
        win.set_marker(win.buf.dot)
        put_command_cursor()

# Update one or more windows with buffer contents, where the buffer 
# is explicit, it is a parameter.

def status(buf):
    'Update status line for given buffer in all of its windows'
    for w in windows:
        if w.buf == buf:
            w.update_status()
    if mode == Mode.command:
        put_command_cursor()

# Called at application startup to ensure the frame is initialized only once.
# The same application may be started, exited, started again several times
# during a single interactive Python session.
# text.buf must already exist when this is called.

def startup(cmd_h, buf):
    'Initialize frame at application startup with window into buf'
    if not win: # create initial window only once in session
        init(cmd_h, buf)
    rescale(cmd_h) # assign cmd_h then refresh display
