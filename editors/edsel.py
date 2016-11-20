"""
edsel - display editor based on the line editor ed.py.  

Described in ed.md and edsel.md.  To run: python3 edsel.py or import edsel then edsel.main()
"""

import traceback, os
import terminal_util, display, window, ed

prompt = '' # command prompt

nlines, ncols = terminal_util.dimensions()

# Default frame dimensions, might be updated while running, especially cmd_h:
frame_top = 1 # line number on display of first line of frame
cmd_h = 2  # height (lines) of scrolling command region at the bottom

# Assigned by calc_frame called from init_session and update_frame
windows_h = None # total number of lines in windows region of frame (all windows)
cmd_1 = None # line number on display of first line of scrolling command region
cmd_n = None #  " bottom "

# First window is assigned from init_session after cmd_h etc. are assigned
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
    'Redraw all windows, called by display_frame, for example after frame resize.'
    for w in windows:
        w.locate_segment_top() # necessary if window(s) resized
        w.update_window(True)  # no windows could be in insert mode at this time

def put_command_cursor():
    'Put cursor at input line in scrolling command region'
    display.put_cursor(cmd_n, 1) # last line on display

def display_frame():
    'Clear and update the entire frame'
    # called from init_session and update_frame
    display.put_cursor(1,1) # origin, upper left corner
    display.erase_display() 
    update_windows()
    win.display_marker()
    display.set_scroll(cmd_1, cmd_n) 
    put_command_cursor()

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
    Clear and render entire display, set scrolling region, place marker.
    Process optional arguments: filename, options if present.
    """
    global prompt, cmd_h, win, win_i
    if filename:
        ed.e(filename[0])
    if 'p' in options:
        prompt = options['p'] 
    if 'c' in options:
        cmd_h = options['c'] 
    # must calc_frame to get window dimensions before we create win
    calc_frame() # assign windows_h etc.
    win = window.Window(ed.buf, frame_top, windows_h, ncols) # one big window
    windows.append(win) 
    win_i = 0 # Now win == windows[win_i]
    display_frame()

# command names used in maintain_display and update_display
ed.cmd_name = '' 

def maintain_display():
    'Maintain consistency in window data after buffer contents change.'
    # Why is this code is so much more complicated than maintaining marks in ed.py?
    # Within ed.py, all of these commands are combinations of just insert i and delete d.
    # ed.py updates buffer immediately for each i and/or d step in each command.
    # But in our design ed.py has no access to display data structures.
    # edsel.py can only observe effects of ed.py command after ed.py has executed it,
    # must infer i and/or d for each command from ed.cmd_name .start .end and buf.nlines.
    for w in windows:
        # adjust dot in other windows into current buffer
        if (w != win and w.buf == win.buf):
            dot0 = w.dot # DEBUG - save initial value for print, below
            if ed.cmd_name in 'aiyr': # insert commands (not including c)
                if ed.start <= w.dot:
                    w.dot += w.buf.nlines
            elif ed.cmd_name == 't': # transfer (copy)
                if ed.dest < w.dot:
                    w.dot += w.buf.nlines
            elif ed.cmd_name in 'dc': # delete or change (replace), del then insert
                # c command: first ed.do_command() calls buf.d, the rest call buf.a
                #  but ed.cmd_name is 'c' until final . exits insert mode
                # This code will not work for c() in API.
                if ed.start < w.dot and ed.end < w.dot: # del or change before w.dot
                    w.dot += w.buf.nlines # nlines here might be negative
                elif ed.start <= w.dot <= ed.end: # change segment includes w.dot
                    w.dot = w.buf.dot
            elif ed.cmd_name == 'm': # move, delete then yank
                # segment follows dot, after move precedes dot
                if ed.start > w.dot > ed.dest:
                    w.dot += w.buf.nlines
		# segment precedes dot, after move follows dot
                elif ed.start < w.dot < ed.dest and ed.end < w.dot:
                    w.dot -= w.buf.nlines # move nlines is positive
	        # dot lies within segment, moves along with segment
                elif ed.start <= w.dot <= ed.end:
                    if ed.dest >= w.dot:  # destination follows w.dot
                        w.dot = (ed.dest - w.buf.nlines) + (w.dot - ed.start) + 1
                    else: # destination precedes w.dot
                        w.dot = ed.dest + (w.dot - ed.start) + 1
            # else... is implicit, all other cases: don't adjust w.dot
            w.dot = w.dot if w.dot > 0 else 1
            w.dot = w.dot if w.dot <= w.buf.S() else w.buf.S()
            # In insert mode, this DEBUG print appears in window, is rapidly overwritten
            #print('w %s  start %s  end %s  dest %s  nlines %s  dot0 %s  dot %s' %
            #     (w, ed.start, ed.end, ed.dest, w.buf.nlines, dot0, w.dot)) # DEBUG
    win.buf.nlines = 0 # FIXME? Put this in cmd with clear_flags ?

# command names used in update_display
o_cmd = '' # also ed.cmd_name, initialized above

# command name categories used in update_display
file_cmds = 'eEfB' # change file displayed in current window
buffer_cmds = 'bB' # change buffer displayed in current window
text_cmds = 'aicdsymtr' # change text displayed in current window

# previous values used in update_display
cmd_h0 = win0 = None

def update_display():
    'Check for any needed display updates.  If there are any, do them.'
    win.dot = win.buf.dot # dot may or may not have changed, update anyway
    win.locate_dot() # assign new dot_i, only in current winow
    segment_moved = (ed.cmd_name in file_cmds + buffer_cmds
                     or win.dot_elsewhere() 
                     or o_cmd in ('o1','o2')) # set single window or split
    # frame changed, update all windows and marker
    if cmd_h != cmd_h0:
        update_frame()  # calls display_frame, which calls update_windows

    # set other window
    elif o_cmd == 'o': 
        # move marker to new current window, don't update window content
        win0.locate_dot()
        win0.erase_marker()
        win.display_marker()

    # update current window contents, maybe other windows too
    elif segment_moved or ed.cmd_name in text_cmds:
        if segment_moved:
            win.locate_segment_top()
        win.update_window(ed.command_mode)
        if o_cmd == 'o2': # split window
            # win0 is former current window
            # if win0 marker does not lie within new window erase it now.
            # win.resize in o2 command code does not relocate win0 marker
            if win0.dot_i < win.win_1 or win0.dot_i > win.win_1+win.win_h:
                win0.erase_marker()
                win0.locate_segment_top() # necessary?
            win0.update_window(True)
        else:  # other non-current windows might show part of same buffer
            for w in windows:
                if (w != win and w.buf == win.buf):
                    # might update even when lines in w unchanged
                    # win0.locate_segment_top() # necessary?
                    w.update_window(True)
        # must draw marker or cursor last
        if ed.command_mode:
            win.display_marker() # indicates dot in window
        else: 
            win.put_insert_cursor() # term. insert cursor at open line

    # update marker only in current window, don't update window content
    elif win.dot_moved():
        win.erase_marker()
        win.display_marker()
        win.display_status()

    # some commands do not affect windows or status line: A k n w ... 

    # put ed command cursor back in scrolling command region
    if ed.command_mode:
        put_command_cursor() 

def restore_display():
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
        else:
            ed.do_command(line) # non-blocking
            if ed.cmd_name in 'bBeED':
                win.buf = ed.buf # ed.buf might have changed
        maintain_display() # maintain consistency in window data 
        update_display() # contains all update logic, may do nothing
    except BaseException as e:
        restore_display() # so we can see entire traceback 
        traceback.print_exc() # looks just like unhandled exception
        exit()

# Configure ed (imported above) to work with edsel
# Suppress printing ed l z command output to scrolling command region
ed.print_lz_destination = open(os.devnull, 'w') # discard output
# In ed x command use edsel.cmd in this module that calls update_display
ed.x_cmd_fcn = do_command

def main(*filename, **options):
    """
    Top level edsel command to invoke from python prompt or command line.
    Won't cooperate with Piety scheduler, calls blocking command raw_input.
    """
    ed.quit = False # allow restart
    init_session(*filename, **options)
    while not ed.quit:
        prompt_string = prompt if ed.command_mode else ''
        line = input(prompt_string) # blocking
        do_command(line) # no blocking
    restore_display()

# Run the editor from the system command line: python edsel.py
if __name__ == '__main__':
    # import argparse inside if ... so it isn't always a dependency of this module
    # duplicates code from ed.py but that is the cost of avoiding dependency on argparse.
    import argparse
    parser = argparse.ArgumentParser(description='display editor in pure Python based on the line editor ed.py')
    parser.add_argument('file', 
                        help='name of file to load into main buffer at startup (omit to start with empty main buffer)',
                        nargs='?',
                        default=None),
    parser.add_argument('-p', '--prompt', help='command prompt string (default no prompt)',
                        default='')
    parser.add_argument('-c', '--cmd_h', help='number of lines in scrolling command region (default 2)',
                        type=int, default=2)
    args = parser.parse_args()
    filename = [args.file] if args.file else []
    options = {'p': args.prompt } if args.prompt else {}
    options.update({'c': args.cmd_h } if args.cmd_h else {})
    main(*filename, **options)
