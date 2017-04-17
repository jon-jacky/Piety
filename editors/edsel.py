"""
edsel - display editor based on the line editor ed.py.  

Described in ed.md and edsel.md.  To run: python3 edsel.py or import edsel then edsel.main()
"""

import traceback, os
import terminal_util, display, window, ed, frame

nlines, ncols = terminal_util.dimensions()

# Default frame dimensions, might be updated while running, especially cmd_h:
frame_top = 1 # line number on display of first line of frame
cmd_h = 2  # height (lines) of scrolling command region at the bottom

# Assigned by calc_frame called from startup and update_frame
windows_h = None # total number of lines in windows region of frame (all windows)
cmd_1 = None # line number on display of first line of scrolling command region
cmd_n = None #  " bottom "

# First window is assigned from startup after cmd_h etc. are assigned
win_i = None # current window index
win = None # current window
windows = list() # list of windows, windows[win_i] is the current window

def calc_frame():
    'Calculate dimensions and location of windows and scrolling command region'
    global cmd_1, cmd_n, windows_h
    cmd_1 = nlines - cmd_h + 1 # scrolling cmd region, index of first line
    cmd_n = nlines # last line on display
    windows_h = nlines - cmd_h # text window fills remaining space

def update_windows():
    'Redraw all windows, called by render_frame, for example after frame resize.'
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

# ed command names used in update_display - FIXME use Op
ed.cmd_name = '' 

# edsel command names used in update_display
o_cmd = '' # also ed.cmd_name, initialized above

# ed command name categories used in update_display - FIXME should use Op
file_cmds = 'eEfB' # change file displayed in current window
buffer_cmds = 'bB' # change buffer displayed in current window
text_cmds = 'aicdsymtr' # change text displayed in current window

# previous values used in update_display
cmd_h0 = win0 = None

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

def cleanup():
    'Restore full-screen scrolling, cursor to bottom.'
    display.set_scroll_all()
    display.put_cursor(nlines,1)

def o(line):
    'Window commands.  These are handled here, they are not not passed to ed.'
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

    # o1: return to single window
    elif param_string.startswith('1'):
        o_cmd = 'o1'
        # delete all but current window
        windows = [windows[win_i]]
        win_i = 0
        win = windows[win_i]
        win.resize(frame_top, windows_h, ncols) # one big window

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
    # maybe more options later
    else:
        print('? integer 1 or 2 expected at %s' % param_string)

def do_command(line):
    'Process one command line without blocking.'
    global cmd_h0, win0, o_cmd
    # try/except ensures we restore display, especially scrolling
    try:
        cmd_h0, win0 = cmd_h, win # save parameters before call ed.cmd
        o_cmd = ed.cmd_name = ''  # must clear before call ed.cmd
        # Intercept special commands used by edsel only, not ed
        # Only in command mode!  Otherwise line is text to add to buffer.
        if ed.command_mode and line.lstrip().startswith('o'):
            o(line) # window commands, assigns o_cmd
            # FIXME: force update, later this will replace o_cmd 
            frame.update(frame.Op.window)
        else:
            ed.do_command(line) # non-blocking
            if ed.cmd_name in 'bBeED':
                win.buf = ed.buf # ed.buf might have changed
        while frame.updates: # process pending updates from all tasks
            update = frame.updates.popleft()
            adjust_segments(update) # shift to adjust for insert/delete
            update_display(update) # contains all update logic, may do nothing
    except BaseException as e:
        cleanup() # so we can see entire traceback 
        traceback.print_exc() # looks just like unhandled exception
        exit()

def startup(*filename, **options):
    global cmd_h, win, win_i
    # must call configure() first, startup() uses update_fcn 
    ed.configure(cmd_fcn=do_command, # so x uses edsel not ed do_command()
                 print_dest=open(os.devnull, 'w'), # discard l z printed output
                 update_fcn=frame.update) # post display updates
    ed.startup(*filename, **options)
    if 'c' in options:
        cmd_h = options['c'] 
    calc_frame() # must assign windows_h etc. before we create first window
    win = window.Window(ed.buf, frame_top, windows_h, ncols) # one big window
    windows.append(win) 
    win_i = 0 # Now win == windows[win_i]
    render_frame()

def main(*filename, **options):
    """
    Top level edsel command to invoke from python prompt or command line.
    Won't work with Piety cooperative multitasking, calls blocking input().
    """
    startup(*filename, **options)
    while not ed.quit:
        prompt_string = ed.prompt if ed.command_mode else ''
        line = input(prompt_string) # blocking
        do_command(line) # no blocking
    cleanup()

if __name__ == '__main__':
    filename, options = ed.cmd_options()
    main(*filename, **options)
