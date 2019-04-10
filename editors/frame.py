"""
frame.py - Multiwindow display implemented by a list of window instances,
            with a scrolling command region at the bottom of the display.
"""

from enum import Enum
import terminal, terminal_util, display, window
from updates import Op, background_task

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
    display = 3 # eden display mode

mode = Mode.command
window.show_marker = True

def scale(nlines, cmd_h):
    'Calculate dimensions and location of windows and scrolling command region'
    global cmd_1, cmd_n, windows_h
    cmd_1 = nlines - cmd_h + 1 # scrolling command region, index of first line
    cmd_n = nlines # scrolling command region, last line
    windows_h = nlines - cmd_h # windows with status lines fill remaining space

def init(buffer):
    'Initialize frame with one window into buffer'
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
        if w.focus and mode == Mode.command:
            w.set_marker(w.buf.dot)

def put_command_cursor(column=1):
    'Put cursor at input line in scrolling command region, at given column'
    display.put_cursor(cmd_n, column) # last line on display

def put_display_cursor(column=1):
    wdot = win.wline(win.buf.dot)
    display.put_cursor(wdot,column)

def refresh(column=1):
    'Clear and update entire frame in command mode, otherwise just the windows'
    if mode == Mode.command:
        display.put_cursor(1,1) # upper left corner
        display.erase()
    update_windows()
    if mode == Mode.command:
        display.set_scroll(cmd_1, cmd_n)
        # update() sets cursor
    elif mode == Mode.display:
        put_display_cursor(column=column)

def rescale():
    'Recalculate frame and all window dimensions, then display all.'
    # Makes all windows (almost) the same height, unlike after o2 command
    scale(nlines, cmd_h)
    nwindows = len(windows)
    win_hdiv = windows_h // nwindows
    for iwin, win in enumerate(windows):
        win_h = (win_hdiv if iwin < nwindows-1
                 else windows_h - (nwindows-1)*win_hdiv) # including status
        win.resize(frame_top + iwin*win_hdiv, win_h-1, ncols) # -1 excl status
        win.locate_segment(win.buf.dot if win.focus else win.saved_dot)
    refresh()

def update(op, sourcebuf=None, buffer=None, origin=0, destination=0,
           start=0, end=0, column=1): # display column numbers are 1-based
    'Update the display: one window, several, or the entire frame.'

    global mode, win, ifocus, cmd_h

    # Clear display, redraw all the windows and scrolling command region.
    if op == Op.refresh:
        refresh(column=column)

    # Restore full screen scrolling, cursor to bottom
    elif op == Op.restore:
        display.set_scroll_all()
        display.put_cursor(nlines,1)

    # Rescale frame and window sizes, then refresh.
    elif op == Op.rescale:
        cmd_h = start if start else cmd_h
        rescale()

    # Create new buffer, ed B, Op.insert case will display its contents.
    elif op == Op.create:
        win.focus = True
        win.buf = buffer
        win.locate_segment(win.buf.dot)
        win.saved_dot = win.buf.dot
        win.reupdate()

    # Change buffer in current window, ed b E D
    elif op == Op.select:
        win.focus = True
        win.buf = buffer
        win.reupdate()

    # Delete current buffer, ed D
    elif op == Op.remove:
        for w in windows:
            if w.buf == sourcebuf: # deleted buffer
                w.buf = buffer     # new current buffer
                w.reupdate()

    # Switch to ed input mode, for ed a i c commands
    elif op == Op.input:
        mode = Mode.input
        window.show_marker = False
        win.update_for_input()
        wdot = win.wline(win.buf.dot)
        display.put_cursor(wdot+1,1)

    # Switch to ed command mode, ed . while in input mode
    elif op == Op.command:
        mode = Mode.command
        window.show_marker = True
        # Overwrite '.' line on display, and lines below.
        win.update_from(win.buf.dot + 1)
        win.set_marker(win.buf.dot)

    # Switch to eden display mode
    elif op == Op.display:
        mode = Mode.display
        window.show_marker = False
        put_display_cursor(column=column)

    # Dot moved, ed l command
    elif op == Op.locate:
        win.locate(origin, destination)

    # Insert text: ed a i c m r t y commands
    # start, end are after insert, start == destination, end == win.buf.dot
    elif op == Op.insert and origin != background_task:
        if mode != Mode.input: # ed commands m r t y
            win.insert(origin, start, end)
        elif mode == Mode.input: # input mode after ed commands a i c
            # Text at dot is already up-to-date on display, open next line.
            win.update_for_input()
        for w in windows:
            if w.samebuf(win):
                w.adjust_insert(start, end, destination)
        if mode == Mode.input: # can't put input cursor til other windows done
            win.put_cursor_for_input(column=1)

    # Background task inserts text by calling buffer write() method.
    # Search for windows (if any) which displays that buffer.
    elif op == Op.insert and origin == background_task:
        for w in windows:
            if w.buf == buffer:
                w.saved_dot = w.buf.dot
                terminal.set_line_mode()
                w.insert(origin, start, end)
                terminal.set_char_mode()
        if mode == Mode.input: # can't put input cursor til other windows done
            win.put_cursor_for_input(column=column)
        elif mode == Mode.display:
            put_display_cursor(column=column)
        else:
            pass # Mode.commmand handled at the end of this fcn

    # Delete text: ed d m command
    # start,end are line numbers before delete, destination == win.buf.dot
    elif op == Op.delete:
        win.delete(destination)
        for w in windows:
            if w.samebuf(win):
                w.adjust_delete(start, end, destination)
 
    # Change text: ed s command
    # Update all lines in start..destination, don't know which lines changed
    elif op == Op.mutate:
        win.mutate(origin, start, destination)
        for w in windows:
            if w.samebuf(win):
                if w.intersects(start, destination):
                    w.mutate_lines(start, destination)

    # Switch to next window, edsel o command
    elif op == Op.next:
        w0 = win
        w0.release_focus()
        w0.update_status()
        ifocus = ifocus+1 if ifocus+1 < len(windows) else 0
        win = windows[ifocus]
        win.set_focus()
        win.update_status()

    # Delete all but current window, edsel o1 cmd
    elif op == Op.single: 
        windows[:] = [win]
        ifocus = 0
        win.resize(frame_top, windows_h-1, ncols) # one window, -1 excl status
        win.reupdate()

    # Split window, new window above becomes current window, edsel o2 command
    elif op == Op.hsplit:
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

    # Update status line for given buffer in all of its windows
    elif op == Op.status:
        for w in windows:
            if w.buf == buffer:
                w.update_status()

    # In command mode put ed command cursor back in scrolling command region.
    # Then we can call standard Python input() or Piety Console restart().
    if mode == Mode.command:
        put_command_cursor(column=column) # background task can set column
    # Each Op... case handles other modes, see refresh() and Op.refresh
    # Is that necessary? I recall it's because some cases use default column=1

    return win # caller might need to know which window was selected
