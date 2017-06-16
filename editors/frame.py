"""
frame.py - Multiwindow display implemented by a list of window instances,
            with a scrolling command region at the bottom of the display.

Just a module, not a class.  We expect only a single frame in a session.
"""

import terminal_util, display, window
from update import updates, Op, placeholder

nlines, ncols = terminal_util.dimensions()

# Default frame dimensions, might be updated while running, especially cmd_h:
frame_top = 1 # line number on display of first line of frame
cmd_h = 2  # default height (lines) of scrolling command region at the bottom

# Assigned by calc_frame called from startup and update_frame
windows_h = None # total number of lines in windows region of frame (all windows)
cmd_1 = None # line number on display of first line of scrolling command region
cmd_n = None #  " bottom "

# First window is assigned from startup after cmd_h etc. are assigned
win_i = None # current window index
win = None # current window
windows = list() # list of windows, windows[win_i] is the current window

# Control state variables
command_mode = True # alternates with input (insert) mode used by ed a,i,c cmds

# previous values used in update_display
cmd_h0 = None

def calc_frame():
    'Calculate dimensions and location of windows and scrolling command region'
    global cmd_1, cmd_n, windows_h
    cmd_1 = nlines - cmd_h + 1 # scrolling cmd region, index of first line
    cmd_n = nlines # last line on display
    windows_h = nlines - cmd_h # text window fills remaining space

def update_windows():  # update_all_windows
    'Redraw all windows, called by render_frame, for example after resize.'
    for w in windows:
        w.update_lines(w.win_1, w.seg_1)
        if w.current:
            w.set_marker(w.buf2win(w.buf.dot), w.buf.dot)
        w.render_status_info(placeholder) # DIAGNOSTIC

def put_command_cursor():
    'Put cursor at input line in scrolling command region'
    display.put_cursor(cmd_n, 1) # last line on display

def render_frame():
    'Clear and update the entire frame'
    # called from startup and update_frame
    display.put_cursor(1,1) # origin, upper left corner
    display.erase() 
    update_windows()
    display.set_scroll(cmd_1, cmd_n) 
    put_command_cursor()

def update_frame():
    'Recalculate frame and all window dimensions, then display all.'
    # Makes all windows (almost) the same height, unlike after o2 command
    calc_frame() # recalculate global cmd_1 cmd_n windows_h
    nwindows = len(windows)
    win_hdiv = windows_h // nwindows # integer division
    for iwin, win in enumerate(windows):
        win_h = win_hdiv if iwin < nwindows-1 else windows_h - (nwindows-1)*win_hdiv
        win.resize(frame_top + iwin*win_hdiv, win_h, ncols)
    render_frame()

def update_display(update):
    global command_mode, windows, win, win_i

    # frame changed, update all windows and markers
    if cmd_h != cmd_h0: # FIXME should be an Op case, eliminate cmd_h0
        update_frame()  # calls render_frame, which calls update_windows

    # Op cases 
    # Placeholder
    elif update.op == Op.nop:
        pass 

    # Create new buffer, ed B, Op.insert case will display its contents
    if update.op == Op.create:
        win.current = True
        win.buf = update.buffer

    # Change buffer in current window, ed b E D
    elif update.op == Op.select:
        win.current = True
        win.buf = update.buffer
        # These four lines occur again and again
        win.locate_segment(win.buf.dot)
        win.update_lines(win.win_1, win.seg_1)
        win.set_marker(win.buf2win(win.buf.dot), win.buf.dot)
        win.render_status_info(update) # DIAGNOSTIC

    # Switch to input (insert) mode, for ed a i c commands
    elif update.op == Op.input:
        command_mode = False 
        win.update_for_input()
        win.render_status_info(update) # DIAGNOSTIC
        display.put_cursor(win.dot_i+1,1)

    # Switch to command mode, ed . while in input mode
    elif update.op == Op.command:
        command_mode = True
        # Overwrite '.' line on display, and lines below.
        win.update_lines(win.dot_i+1, win.buf.dot+1)
        win.set_marker(win.dot_i, win.buf.dot)
        win.render_status_info(update) # DIAGNOSTIC

    # Dot moved, ed l command
    elif update.op == Op.locate:
        # Later move all this to window method, 
        if win.contains(update.destination):
            win.clear_marker(win.buf2win(update.origin), update.origin)
        else:
            # The following four lines appear in Op.single,.hsplit, make method
            win.locate_segment(update.destination)
            win.update_lines(win.win_1, win.seg_1)
        win.set_marker(win.buf2win(update.destination), update.destination)
        win.render_status_info(update) # DIAGNOSTIC, not included in win.locate

    # Insert text: ed a i c m r t y commands
    elif update.op == Op.insert:
        # update.start, end are the first, last inserted line
        # win.buf.dot is the last inserted line
        if command_mode: # ed commands m r t y
            if win.contains(update.end):
                if update.origin != 0:
                    win.clear_marker(win.buf2win(update.origin), update.origin)
                win.update_lines(win.buf2win(update.start), update.start)
            else:
                win.locate_segment(update.end)
                win.update_lines(win.win_1, win.seg_1)
            win.set_marker(win.buf2win(update.end), update.end)
        else: # input mode after ed commands a i c    
            # Text at dot is already up-to-date on display.
            # Open next line and overwite lines below, scroll up if needed.
            win.update_for_input()
        win.render_status_info(update) # DIAGNOSTIC
        for w in windows:
            if (w != win and w.buf == win.buf): # other windows, current buffer
                #FIXME?Does this assumes only one line inserted?
                if w.contains(update.end): # does this assume nlines == 1 ?
                    w.update_lines(w.buf2win(update.end), update.end)
                    w.render_status_info(update) # DIAGNOSTIC
                elif w.seg_1 > update.end: # inserted text above window
                    nlines = (update.end - update.start) + 1
                    w.shift(nlines)  # does this assume update.nlines==1
                    w.render_status_info(update) # DIAGNOSTIC
                else: # inserted text below window
                    pass
        if not command_mode:
            display.put_cursor(win.dot_i+1,1)

    # Delete text: ed d m commands
    elif update.op == Op.delete:
        if win.contains(update.destination):
            win.update_lines(win.buf2win(update.destination), 
                             update.destination)
        else:
            win.locate_segment(update.destination)
            win.update_lines(win.win_1, win.seg_1)
        win.set_marker(win.buf2win(update.destination), update.destination)
        win.render_status_info(update) # DIAGNOSTIC
        for w in windows:
            if (w != win and w.buf == win.buf): # other windows, current buffer
                if w.contains(update.destination):
                    w.update_lines(w.buf2win(update.destination), 
                                   update.destination)
                    w.render_status_info(update) # DIAGNOSTIC
                elif w.seg_1 > update.destination: # deleted text above window
                    nlines = (update.end - update.start) + 1
                    w.shift(-nlines)
                    w.render_status_info(update) # DIAGNOSTIC
                else: # deleted text below window
                    pass

    # Switch to next window, edsel o command
    elif update.op == Op.next:
        # Save current buffer dot in window saved dot
        win0 = win
        win0.current = False
        win0.dot = win0.buf.dot #FIXME rename lhs win.saved_dot
        win_i = win_i+1 if win_i+1 < len(windows) else 0
        win = windows[win_i] # assign new window
        win.current = True
        # Restore new window saved dot to buffer dot 
        win.buf.dot = win.dot # FIXME rename rhs win.saved_dot
        win0.clear_marker(win0.buf2win(win0.dot),win0.dot) # win0.saved_dot
        win.set_marker(win.buf2win(win.buf.dot), win.buf.dot)
        win.render_status_info(update) # DIAGNOSTIC

    # Delete all but current window, edsel o1 cmd
    elif update.op == Op.single: 
        windows = [win]
        win_i = 0
        win.resize(frame_top, windows_h, ncols) # one big window
        # The following four lines appear in Op.hsplit also - window method
        win.locate_segment(win.buf.dot)
        win.update_lines(win.win_1, win.seg_1)
        win.set_marker(win.buf2win(win.buf.dot), win.buf.dot)
        win.render_status_info(update) # DIAGNOSTIC

    # Split window, new window above becomes current window, edsel o2 command
    elif update.op == Op.hsplit: 
        win0 = win
        win0.current = False
        win0.dot = win0.buf.dot  # FIXME lhs: win0.saved_dot
        win_top = win0.win_1
        new_win_h = win0.win_h // 2 # integer division
        win0.resize(win_top + new_win_h, win0.win_h - new_win_h, ncols) # old
        win = window.Window(win.buf, win_top, new_win_h, ncols) # new window
        win.current = True
        windows.insert(win_i, win)
        # The following four lines appear in Op.single also - window method
        win.locate_segment(win.buf.dot)
        win.update_lines(win.win_1, win.seg_1)
        win.set_marker(win.buf2win(win.buf.dot), win.buf.dot)
        win.render_status_info(update) # DIAGNOSTIC
        # Here are those same four lines again - should be a window method
        # EXCEPT here we clear marker instead of set it.
        win0.locate_segment(win0.buf.dot)
        win0.update_lines(win0.win_1, win0.seg_1)
        win0.clear_marker(win0.buf2win(win0.buf.dot), win0.buf.dot)
        win0.render_status_info(update) # DIAGNOSTIC

    # put ed command cursor back in scrolling command region
    if command_mode:
        put_command_cursor() 

def init(buffer, cmd_h_option=None):
    'Initialize frame with one window into buffer'
    global cmd_h, win, win_i
    if cmd_h_option: 
        cmd_h = cmd_h_option # otherwise keep default assigned above
    calc_frame() # must assign windows_h etc. before we create first window
    win = window.Window(buffer, frame_top, windows_h, ncols)
    win.current = True
    windows.append(win) 
    win_i = 0 # Now win == windows[win_i]
    render_frame()

def handle_updates():
    'Process display update records from queue'
    while updates:
        update = updates.popleft()
        update_display(update)
