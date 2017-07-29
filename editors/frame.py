"""
frame.py - Multiwindow display implemented by a list of window instances,
            with a scrolling command region at the bottom of the display.
"""

import terminal_util, display, window
from updates import Op

nlines, ncols = terminal_util.dimensions()

# Default frame dimensions, might be updated while running, especially cmd_h:
frame_top = 1 # line number on display of first line of frame
cmd_h = 2  # default height (lines) of scrolling command region at the bottom

# Assigned by scale()
windows_h = None # total number of lines of all windows, including status lines
cmd_1 = None # line number on display of first line of scrolling command region
cmd_n = None #  " bottom "

# First window is assigned from startup after cmd_h etc. are assigned
win_i = None # current window index
win = None # current window
windows = list() # list of windows, windows[win_i] is the current window

# Control state variables
command_mode = True # alternates with input (insert) mode used by ed a,i,c cmds

def scale(nlines, cmd_h):
    'Calculate dimensions and location of windows and scrolling command region'
    global cmd_1, cmd_n, windows_h
    cmd_1 = nlines - cmd_h + 1 # scrolling command region, index of first line
    cmd_n = nlines # scrolling command region, last line
    windows_h = nlines - cmd_h # windows with status lines fill remaining space

def init(buffer, cmd_h_option=None):
    'Initialize frame with one window into buffer'
    global cmd_h, win, win_i
    if cmd_h_option: 
        cmd_h = cmd_h_option # otherwise keep default assigned above
    scale(nlines, cmd_h) # must assign frame size before create first window
    win = window.Window(buffer, frame_top, windows_h-1, ncols) # -1 excl status
    win.current = True
    windows.append(win) 
    win_i = 0

def update_windows():
    'Redraw all windows, called by refresh, for example after resize.'
    for w in windows:
        w.update()
        if w.current:
            w.set_marker(w.buf.dot)

def put_command_cursor():
    'Put cursor at input line in scrolling command region'
    display.put_cursor(cmd_n, 1) # last line on display

def refresh():
    'Clear and update the entire frame'
    display.put_cursor(1,1) # upper left corner
    display.erase() 
    update_windows()
    display.set_scroll(cmd_1, cmd_n) 
    put_command_cursor()

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
    refresh()

def update(op, buffer, origin, destination, start, end):
    """
    Update the display: one window, several, or the entire frame.
    Arguments here are the fields of the UpdateRecord namedtuple.
    Other data used here are already stored in the frame, windows, and buffers.
    """
    global command_mode, win, win_i

    # Clear display, redraw all the windows and scrolling command region.
    if op == Op.refresh:
        refresh()

    # Rescale frame and window sizes, then refresh.
    if op == Op.rescale:
        rescale()

    # Create new buffer, ed B, Op.insert case will display its contents.
    elif op == Op.create:
        win.current = True
        win.buf = buffer

    # Change buffer in current window, ed b E D
    elif op == Op.select:
        win.current = True
        win.buf = buffer
        win.reupdate()

    # Switch to input (insert) mode, for ed a i c commands
    elif op == Op.input:
        command_mode = False 
        win.update_for_input()
        wdot = win.wline(win.buf.dot)
        display.put_cursor(wdot+1,1)

    # Switch to command mode, ed . while in input mode
    elif op == Op.command:
        command_mode = True
        # Overwrite '.' line on display, and lines below.
        win.update_from(win.buf.dot + 1)
        win.set_marker(win.buf.dot)

    # Dot moved, ed l command
    elif op == Op.locate:
        if win.contains(destination):
            win.clear_marker(origin)
            win.set_marker(destination)
            win.update_status()
        else:
            win.reupdate()

    # Insert text: ed a i c m r t y commands
    # start, end are after insert, start == destination
    # end == win.buf.dot
    elif op == Op.insert:
        if command_mode: # ed commands m r t y
            if win.contains(end):
                if origin != 0:
                    win.clear_marker(origin)
                win.update_from(start)
            else:
                win.reupdate()
        else: # input mode after ed commands a i c    
            # Text at dot is already up-to-date on display, open next line.
            win.update_for_input()
        for w in windows:
            if (w != win and w.buf == win.buf):
                w.adjust_segment(start, end, destination)
        if not command_mode:
            wdot = win.wline(win.buf.dot)
            display.put_cursor(wdot+1,1)

    # Delete text: ed d m command
    # start,end are line numbers before delete, destination==win.buf.dot
    elif op == Op.delete:
        if win.might_contain(destination): # window already contains new dot
            win.update_from(destination)
            win.set_marker(destination)
        else:
            win.reupdate() 
        for w in windows:
            if (w != win and w.buf == win.buf):
                w.adjust_segment(start, end, destination,
                                 delete=True)
 
    # Change text: ed s command
    # Update all lines in start..end, we don't know which lines changed,
    # except destination == end is the last line actually changed.
    elif op == Op.mutate:
        if win.contains(destination):
            # FIXME? If origin not in window, does this do nothing, or crash?
            win.clear_marker(origin)
            top = max(start, win.btop)
            win.update_lines(win.wline(top), top, 
                             last=win.wline(destination))
            win.update_status()
            win.set_marker(destination)
        else:
            win.reupdate()
        for w in windows:
            if (w != win and w.buf == win.buf):
                if w.intersects(start, destination):
                    # FIXME: almost repeats code in win. case above
                    top = max(start, win.btop)
                    w.update_lines(w.wline(top), top, 
                                   last=w.wline(destination))
                    w.update_status()

    # Switch to next window, edsel o command
    elif op == Op.next:
        w0 = win
        w0.current = False
        w0.saved_dot = w0.buf.dot
        w0.clear_marker(w0.saved_dot)
        win_i = win_i+1 if win_i+1 < len(windows) else 0
        win = windows[win_i]
        win.current = True
        win.buf.dot = win.saved_dot
        win.set_marker(win.buf.dot)
        win.update_status()

    # Delete all but current window, edsel o1 cmd
    elif op == Op.single: 
        windows[:] = [win]
        win_i = 0
        win.resize(frame_top, windows_h-1, ncols) # one window, -1 excl status
        win.reupdate()

    # Split window, new window above becomes current window, edsel o2 command
    elif op == Op.hsplit: 
        win_top = win.top
        win_nlines = win.nlines // 2
        w0 = win
        w0.current = False
        w0.saved_dot = w0.buf.dot
        w0.resize(win_top + win_nlines, w0.nlines - win_nlines, ncols)
        w0.move_update(w0.saved_dot)
        w0.clear_marker(w0.saved_dot)
        win = window.Window(win.buf,win_top,win_nlines-1,ncols) #-1 excl status
        win.current = True
        windows.insert(win_i, win)
        win.reupdate()

    # Put ed command cursor back in scrolling command region
    if command_mode:
        put_command_cursor() 
