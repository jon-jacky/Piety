"""
frame.py - Multiwindow display implemented by a list of window instances,
            with a scrolling command region at the bottom of the display.
"""

from enum import Enum
import terminal, terminal_util, display, window
from updates import Op, background_task

# Data structures

nlines, ncols = terminal_util.dimensions()

# Default frame dimensions, might be updated while running, especially cmd_h:
frame_top = 1 # line number on display of first line of frame
cmd_h = 2  # default height (lines) of scrolling command region at the bottom

# Assigned by scale()
windows_h = None # total number of lines of all windows, including status lines
cmd_1 = None # line number on display of first line of scrolling command region
cmd_n = None #  " bottom "

# First window is assigned from startup after cmd_h etc. are assigned
ifocus = None # index of window with input focus
win = None # window with input focus
windows = list() # list of windows, windows[ifocus] has input focus

class Mode(Enum):
    command = 1 # ed command mode
    input = 2   # ed input mode for a,i,c commmands
    display = 3 # edsel display mode

mode = Mode.command
# window.command_mode() tracks mode
window.command_mode = (lambda: mode == Mode.command)

# Helper functions

def scale(nlines, cmd_h):
    'Calculate dimensions and location of windows and scrolling command region.'
    global cmd_1, cmd_n, windows_h
    cmd_1 = nlines - cmd_h + 1 # scrolling command region, index of first line
    cmd_n = nlines # scrolling command region, last line
    windows_h = nlines - cmd_h # windows with status lines fill remaining space

def init(buffer):
    'Initialize frame with one window into buffer.'
    global win, ifocus
    # must assign frame size before create first window
    scale(nlines, cmd_h) # default cmd_h, may reassign before first update
    win = window.Window(buffer, frame_top, windows_h-1, ncols) # -1 excl status
    win.focus = True
    windows.append(win)
    ifocus = 0

def update_windows():
    'Redraw all windows, called by refresh, for example after resize.'
    for w in windows:
        w.update()

# old put cursor fcns called by update

def put_command_cursor(column=1):
    'Put cursor at command line in scroll region, at given column (default 1).'
    display.put_cursor(cmd_n, column) # last line on display

def put_display_cursor(column=1):
    'Put cursor at dot in current window, at given column (default 1).'
    wdot = win.wline(win.buf.dot)
    display.put_cursor(wdot, column)

# new put cursor fcns callded by functions extracted from update

def put_command_cursor_col(column):
    'Put cursor at command line in scroll region, at given column.'
    display.put_cursor(cmd_n, column) # last line on display

def put_command_cursor_c1():
    'Put cursor at command line in scroll region, at column 1.'
    display.put_cursor(cmd_n, 1) # last line on display

def put_display_cursor_col(column):
    'Put cursor at dot in current window, at given column.'
    wdot = win.wline(win.buf.dot)
    display.put_cursor(wdot, column)

def put_display_cursor_c1():
    'Put cursor at dot in current window, at column 1.'
    wdot = win.wline(win.buf.dot)
    display.put_cursor(wdot, 1)

# Display update functions called by clients
#    global mode, win, ifocus, cmd_h

def refresh(column):
    """
    Clear, update entire display in command mode, otherwise just the windows.
    column is where to put cursor, might not be column 1.
    """
    if mode == Mode.command:
        display.put_cursor(1,1) # upper left corner
        display.erase()
    update_windows()
    if mode == Mode.command:
        display.set_scroll(cmd_1, cmd_n)
        put_command_cursor_col(column)
    elif mode == Mode.display:
        put_display_cursor_col(column)

def restore():
    'Restore full screen scrolling, cursor to bottom.'
    display.set_scroll_all()
    display.put_cursor(nlines,1)

def rescale(new_cmd_h):
    """
    Recalculate frame and all window dimensions, then display all.
    new_cmd_h is n of lines in scrolling cmd region, None means no change.
    """
    # Makes all windows (almost) the same height, unlike after o2 command
    global cmd_h
    cmd_h = new_cmd_h if new_cmd_h else cmd_h
    scale(nlines, cmd_h)
    nwindows = len(windows)
    win_hdiv = windows_h // nwindows
    for iwin, win in enumerate(windows):
        win_h = (win_hdiv if iwin < nwindows-1
                 else windows_h - (nwindows-1)*win_hdiv) # including status
        win.resize(frame_top + iwin*win_hdiv, win_h-1, ncols) # -1 excl status
        win.locate_segment(win.buf.dot if win.focus else win.saved_dot)
    refresh(1)

def create(buf):
    'Create new buffer in current window, ed B.'
    win.focus = True
    win.buf = buf
    win.locate_segment(win.buf.dot)
    win.saved_dot = win.buf.dot
    win.reupdate()

def select(buf):
    'Change buffer in current window, ed b E D.'
    win.focus = True
    win.buf = buf
    win.reupdate()
    if mode == Mode.command:
        put_command_cursor_c1()

def remove(delbuf, buf):
    """
    Delete current buffer, ed D.
    delbuf is the deleted buffer, buf is the new current buffer.
    """
    for w in windows:
        if w.buf == delbuf:
            w.buf = buf
            w.reupdate()
    
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
    win.update_from(win.buf.dot + 1)
    win.set_marker(win.buf.dot)
    put_command_cursor_c1()

def display_mode():
    'Switch to edsel display mode'
    global mode
    mode = Mode.display
    win.clear_marker(win.buf.dot)
    put_display_cursor_c1()

def locate(origin, destination):
    'Dot moved, ed l command'
    win.locate(origin, destination)
    if mode == Mode.command:
        put_command_cursor_c1()

def next():
    'Switch to next window, edda o command'
    global ifocus, win
    w0 = win
    w0.release_focus()
    w0.update_status()
    ifocus = ifocus+1 if ifocus+1 < len(windows) else 0
    win = windows[ifocus]
    win.set_focus()
    win.update_status()
    if mode == Mode.command:
        put_command_cursor_c1()
    return win

def single():
    'Delete all but current window, edda o1 cmd'
    global ifocus
    windows[:] = [win]
    ifocus = 0
    win.resize(frame_top, windows_h-1, ncols) # one window, -1 excl status
    win.reupdate()
    put_command_cursor_c1()

def hsplit():
    'Split window, new window above becomes current window, edda o2 command'
    global win
    win_top = win.top
    win_nlines = win.nlines // 2
    w0 = win
    w0.release_focus()
    w0.resize(win_top + win_nlines, w0.nlines - win_nlines, ncols)
    w0.move_update(w0.saved_dot)
    win = window.Window(win.buf,win_top,win_nlines-1,ncols) #-1 excl status
    win.focus = True
    windows.insert(ifocus, win)
    win.reupdate()
    put_command_cursor_c1()

def status(buf):
    'Update status line for given buffer in all of its windows'
    for w in windows:
        if w.buf == buf:
            w.update_status()

def insert(start, end):
    # Insert text: ed a i c m r t y commands
    # start, end are after insert, start == destination, end == win.buf.dot
    if mode != Mode.input: # ed commands m r t y
        win.insert(start, end)
    elif mode == Mode.input: # input mode after ed commands a i c
        # Text at dot is already up-to-date on display, open next line.
        win.update_for_input()
    for w in windows:
        if w.samebuf(win):
            w.adjust_insert(start, end)
    if mode == Mode.input: # can't put input cursor til other windows done
        win.put_cursor_for_input()
    if mode == Mode.command:
        put_command_cursor_c1()

def delete(start, end):
    # Delete text: ed d m command
    # deleted lines were above win.buf.dot
    # we need start, end to adjust the other windows
    win.delete(win.buf.dot)
    for w in windows:
        if w.samebuf(win):
            w.adjust_delete(start, end, win.buf.dot)
    if mode == Mode.command:
        put_command_cursor_c1()

def mutate(start, destination):
    # Change text: ed s command
    # destination is last line where substitution actually made
    # Update all lines in start..destination, don't know which lines changed
    win.mutate(origin, start, destination)
    for w in windows:
        if w.samebuf(win):
            if w.intersects(start, destination):
                w.mutate_lines(start, destination)

def update(op, sourcebuf=None, buffer=None, origin=0, destination=0,
           start=0, end=0, column=1): # display column numbers are 1-based
    'Update the display: one window, several, or the entire frame.'

    global mode, win, ifocus, cmd_h

    # Background task inserts text by calling buffer write() method.
    # Search for windows (if any) which displays that buffer.
    if op == Op.insert and origin == background_task:
        for w in windows:
            if w.buf == buffer:
                w.saved_dot = w.buf.dot
                w.insert(origin, start, end)
        if mode == Mode.input: # can't put input cursor til other windows done
            win.put_cursor_for_input(column=column)
        elif mode == Mode.display:
            put_display_cursor(column=column)
        else:
            pass # Mode.commmand handled at the end of this fcn

    # In command mode put ed command cursor back in scrolling command region.
    # Then we can call standard Python input() or Piety Console restart().
    if mode == Mode.command:
        put_command_cursor(column=column) # background task can set column
    # Each Op... case handles other modes, see refresh() and Op.refresh
    # Is that necessary? I recall it's because some cases use default column=1

    return win # caller might need to know which window was selected
