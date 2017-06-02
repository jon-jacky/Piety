"""
frame.py - Multiwindow display implemented by a list of window instances,
            with a scrolling command region at the bottom of the display.

Just a module, not a class.  We expect only a single frame in a session.
"""

import terminal_util, display, window
from update import update, updates, Op
import ed # FIXME should be able to remove when Op and update queue working

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
command_mode = True # alternates with input (insert) mode used by ed a,i,c commands

# previous values used in update_display
cmd_h0 = win0 = None

# ed command name categories used in update_display - FIXME use Op instead
file_cmds = 'eEfB' # change file displayed in current window
buffer_cmds = 'bB' # change buffer displayed in current window
text_cmds = 'aicdsymtr' # change text displayed in current window

def calc_frame():
    'Calculate dimensions and location of windows and scrolling command region'
    global cmd_1, cmd_n, windows_h
    cmd_1 = nlines - cmd_h + 1 # scrolling cmd region, index of first line
    cmd_n = nlines # last line on display
    windows_h = nlines - cmd_h # text window fills remaining space

def update_windows():  # update_all_windows
    'Redraw all windows, called by render_frame, for example after resize.'
    for w in windows:
        w.position_segment() # necessary if window(s) resized
        w.update()  # no windows could be in insert mode at this time

def put_command_cursor():
    'Put cursor at input line in scrolling command region'
    display.put_cursor(cmd_n, 1) # last line on display

def render_frame():
    'Clear and update the entire frame'
    # called from startup and update_frame
    display.put_cursor(1,1) # origin, upper left corner
    display.erase() 
    update_windows()
    win.render_marker()
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

def reassign_window(update):
    'Assign a different buffer to the current window'
    if update.op in (Op.create, Op.select):
        win.buf = update.buffer

def adjust_segments(update):
    """
    Adust each w.dot .seg_1 .seg_n so that same lines remain at same
    positions in windows even when line numbers change due to deletes
    or inserts above.
    """
    for w in windows:
        if (w != win and w.buf == win.buf): # other windows, current buffer
            w.adjust_segment(update)

def update_other_windows():
    for w in windows:
        if (w != win and w.buf == win.buf):
            # might update even when lines in w unchanged
            # win0.position_segment() # necessary?
            w.update()
                
def update_cursor():
    # extracted from update_affected_windows above
    if command_mode:
        win.render_marker() # indicates dot in window
    else: 
        win.put_insert_cursor() # term. insert cursor at open line

def update_affected_windows(update, segment_moved):
   # extracted from update display under elif segment_moved or ... txt_cmds:
    if segment_moved:
        win.position_segment()
    win.update(open_line=(not command_mode)) # open line in insert mode
    update_other_windows() # other non-current windows might show part of same buffer
    update_cursor() # must draw marker or cursor last

def update_display(update):  # FIXME - use contents of update, an Update record.
    'Check for any needed display updates.  If there are any, do them.'

    # new update_display code that branches on update.op
    # first do window commands o o1 o2, based on old o() fcn
    # merge in more code from below when we untangle logic
    global command_mode, windows, win, win_i

    #print('update_display: ed.cmd_name %s, update.op %s' % 
    #     (ed.cmd_name, update.op)) # DEBUG
    reassign_window(update) # possibly reassign win.buf
    adjust_segments(update) # shift to adjust for insert/delete

    # frame changed, update all windows and marke
    if cmd_h != cmd_h0: # FIXME should be an Op case, eliminate cmd_h0
        update_frame()  # calls render_frame, which calls update_windows

    # Op cases 

    # Switch to input (insert) mode, edsel a i c commands
    if update.op == Op.input:
        command_mode = False 
        win.update_for_input()
        win.render_status_info(update) # DIAGNOSTIC
        display.put_cursor(win.dot_i+1,1)

    # Switch to command mode, edsel . while in input mode
    elif update.op == Op.command:
        command_mode = True
        # Overwrite '.' line on display, and lines below.
        win.update_lines(win.dot_i+1, win.buf.dot+1)
        win.set_marker(win.dot_i, win.buf.dot)
        win.render_status_info(update) # DIAGNOSTIC

    # Insert text in input mode, after edsel a i c commands
    elif update.op == Op.insert and not command_mode:
        # Text at dot is already up-to-date on display.
        # Open next line and overwite lines below, scroll up if needed.
        win.update_for_input()
        win.render_status_info(update) # DIAGNOSTIC
        display.put_cursor(win.dot_i+1,1)

    # Dot moved, edsel l command
    elif update.op == Op.locate:
        # Later move all this to Window method, 
        # here just call win.locate(... source ..., ...destination...)
        if win.contains(update.destination):
            win.clear_marker(win.buf2win(update.start), update.start)
        else:
            # The following four lines appear in Op.single,.hsplit, make method
            win.locate_segment(update.destination)
            win.update_lines(win.win_1, win.seg_1)
        win.set_marker(win.buf2win(update.destination), update.destination)
        win.render_status_info(update) # DIAGNOSTIC, not included in win.locate

    # Switch to next window, edsel o command
    elif update.op == Op.next:
        # Save current buffer dot in window saved dot
        lwin0 = win # lwin0 is local win0 - will replace module level win0 
        lwin0.dot = lwin0.buf.dot #FIXME rename lhs win.saved_dot
        win_i = win_i+1 if win_i+1 < len(windows) else 0
        win = windows[win_i] # assign new window
        # Restore new window saved dot to buffer dot 
        win.buf.dot = win.dot # FIXME rename rhs win.saved_dot
        lwin0.clear_marker(lwin0.buf2win(lwin0.dot),lwin0.dot) #lwin0.saved_dot
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
        lwin0 = win # lwin0 is local win0 - will replace module level win0 
        lwin0.dot = lwin0.buf.dot  # FIXME lhs: lwin0.saved_dot
        win_top = lwin0.win_1
        new_win_h = lwin0.win_h // 2 # integer division
        lwin0.resize(win_top + new_win_h, lwin0.win_h - new_win_h, ncols) # old
        win = window.Window(win.buf, win_top, new_win_h, ncols) # new window
        windows.insert(win_i, win)
        # The following four lines appear in Op.single also - window method
        win.locate_segment(win.buf.dot)
        win.update_lines(win.win_1, win.seg_1)
        win.set_marker(win.buf2win(win.buf.dot), win.buf.dot)
        win.render_status_info(update) # DIAGNOSTIC
        # Here are those same four lines again - should be a window method
        # EXCEPT here we clear marker instead of set it.
        lwin0.locate_segment(lwin0.buf.dot)
        lwin0.update_lines(lwin0.win_1, lwin0.seg_1)
        lwin0.clear_marker(lwin0.buf2win(lwin0.buf.dot), lwin0.buf.dot)
        lwin0.render_status_info(update) # DIAGNOSTIC

    # previous update_display code.  FIXME untangle logic, use Op case analysis
    else:
        win.dot = win.buf.dot # FIXME? dot may or may not have changed, update anyway
        win.find_dot() # FIXME? redundant?  Called again later on all paths?       
        # FIXME break apart this logic into Op case analysis
        segment_moved = (ed.cmd_name in file_cmds + buffer_cmds
                     or win.dot_elsewhere())
                     ### No more ... or o_cmd in (o1,o2)), handled in Op cases above
        # print(' segment_moved %s' % segment_moved) # DEBUG

        # update current window contents, maybe other windows too
        # FIXME break apart this logic into Op case analysis
        if segment_moved or ed.cmd_name in text_cmds:
            update_affected_windows(update, segment_moved)

        # update marker only in current window, don't update window content
        elif win.dot_moved():
            win.erase_marker()
            win.render_marker()
            win.render_status()

    # some commands do not affect windows or status line: A k n w ... 

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
    windows.append(win) 
    win_i = 0 # Now win == windows[win_i]
    render_frame()

def handle_updates():
    'Process display update records from queue'
    while updates:
        update = updates.popleft()
        update_display(update)
