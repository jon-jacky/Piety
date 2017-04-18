"""
frame.py - collection of windows 

Just a module, not a class.  We expect only a single frame in a session.
"""

from enum import Enum
from collections import namedtuple, deque
import terminal_util, display, window
import ed # FIXME should be able to remove when Op and update queue working

class Op(Enum):
    'Generic window operations named independently of particular editor cmds'
    window = 1 # FIXME placeholder for edsel o o1 o2, add more Op values later

Update = namedtuple('Update', ['op','buffer','start','end','dest','nlines'])

updates = deque()

def update(op, buffer=None, start=0, end=0, dest=0, nlines=0):
    'Create an Update record and append it to the updates queue'
    updates.append(Update(op, buffer=buffer, start=start, end=end, dest=dest, 
                          nlines=nlines))

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

# previous values used in update_display
cmd_h0 = win0 = None

# edsel command names used in update_display
o_cmd = '' # also ed.cmd_name, initialized above

# ed command name categories used in update_display - FIXME should use Op
file_cmds = 'eEfB' # change file displayed in current window
buffer_cmds = 'bB' # change buffer displayed in current window
text_cmds = 'aicdsymtr' # change text displayed in current window


def calc_frame():
    'Calculate dimensions and location of windows and scrolling command region'
    global cmd_1, cmd_n, windows_h
    cmd_1 = nlines - cmd_h + 1 # scrolling cmd region, index of first line
    cmd_n = nlines # last line on display
    windows_h = nlines - cmd_h # text window fills remaining space

def update_windows():
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

def adjust_segments(update):
    """
    Adust each w.dot .seg_1 .seg_n so that same lines remain at same
    positions in windows even when line numbers change due to deletes
    or inserts above.
    """
    for w in windows:
        if (w != win and w.buf == win.buf): # other windows, current buffer
            w.adjust_segment(update)

def update_display(update):  # FIXME - use contents of update, an Update record.
    'Check for any needed display updates.  If there are any, do them.'
    win.dot = win.buf.dot # dot may or may not have changed, update anyway
    win.find_dot() # FIXME?  Is this redundant here?  Called again later on all paths?
    segment_moved = (ed.cmd_name in file_cmds + buffer_cmds
                     or win.dot_elsewhere() 
                     or o_cmd in ('o1','o2')) # set single window or split
    # frame changed, update all windows and marker
    if cmd_h != cmd_h0:
        update_frame()  # calls render_frame, which calls update_windows

    # set other window
    elif o_cmd == 'o': 
        # move marker to new current window, don't update window content
        win0.find_dot()
        win0.erase_marker()
        win.render_marker()

    # update current window contents, maybe other windows too
    elif segment_moved or ed.cmd_name in text_cmds:
        if segment_moved:
            win.position_segment()
        win.update(open_line=(not ed.command_mode)) # open line in insert mode
        if o_cmd == 'o2': # split window
            # win0 is former current window
            # if win0 marker does not lie within new window erase it now.
            # win.resize in o2 command code does not relocate win0 marker
            if win0.dot_i < win.win_1 or win0.dot_i > win.win_1+win.win_h:
                win0.erase_marker()
                win0.position_segment() # necessary?
            win0.update()
        else:  # other non-current windows might show part of same buffer
            for w in windows:
                if (w != win and w.buf == win.buf):
                    # might update even when lines in w unchanged
                    # win0.position_segment() # necessary?
                    w.update()
        # must draw marker or cursor last
        if ed.command_mode:
            win.render_marker() # indicates dot in window
        else: 
            win.put_insert_cursor() # term. insert cursor at open line

    # update marker only in current window, don't update window content
    elif win.dot_moved():
        win.erase_marker()
        win.render_marker()
        win.render_status()

    # some commands do not affect windows or status line: A k n w ... 

    # put ed command cursor back in scrolling command region
    if ed.command_mode:
        put_command_cursor() 

def o(line):
    'Window commands.'
    # Not passed to ed, this o() does not conflict with ed.o() that returns dot.
    # For now there is just one vertical stack of windows in the frame.
    global windows, win, win_i, o_cmd
    param_string = line.lstrip()[1:].lstrip()

    # o: switch to next window
    if not param_string:
        o_cmd = 'o' # used by update_display
        win.dot = win.buf.dot # save
        win_i = win_i+1 if win_i+1 < len(windows) else 0
        win = windows[win_i] 
        ed.current = win.buf.name
        ed.buf = ed.buffers[ed.current]
        win.buf.dot = win.dot # restore
        update(Op.window) # FIXME - specialize Op.

    # o1: return to single window
    elif param_string.startswith('1'):
        o_cmd = 'o1'
        # delete all but current window
        windows = [windows[win_i]]
        win_i = 0
        win = windows[win_i]
        win.resize(frame_top, windows_h, ncols) # one big window
        update(Op.window) # FIXME - specialize Op.

    # o2: split window, horizontal
    elif param_string.startswith('2'):
        o_cmd = 'o2'
        # put the new window at the top, it becomes current window
        win_top = win.win_1
        new_win_h = win.win_h // 2 # integer division
        win.resize(win_top + new_win_h, win.win_h - new_win_h, ncols) # old window
        win.dot = win.buf.dot # save
        win = window.Window(ed.buf, win_top, new_win_h, ncols) # new window
        windows.insert(win_i, win)
        update(Op.window) # FIXME - specialize Op.

    # maybe more options later
    else:
        print('? integer 1 or 2 expected at %s' % param_string)

def init(buffer, cmd_h_option):
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
    'Process display update records from update queue'
    # FIXME moved from edsel do_command, can't while loop below get this?
    if ed.cmd_name in 'bBeED':
        win.buf = ed.buf # ed.buf might have changed
    while updates: # process pending updates from all tasks
        update = updates.popleft()
        adjust_segments(update) # shift to adjust for insert/delete
        update_display(update) # contains all update logic, may do nothing
