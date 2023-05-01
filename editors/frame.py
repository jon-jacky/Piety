"""
frame.py - Frame Editor - display buffer contents in a 'frame' of windows
          as they are updated by commands in the sked line editor.
"""

import sys # skip argument declaration has file=sys.stdout
import terminal_util, display
import sked as ed

# Define and initialize global variables used by frame display functions.
# Conditinally exec only the *first* time this module is imported in a session.
# Then we can reload this module without re-initializing those variables.
try:
    _ = flines # if flines is already defined, then frameinit was already exec'd
except:
    exec(open("frameinit.py").read())

# Display functions: building blocks

def update_lines(nlines, bstart, wstart):
    """
    Display consecutive lines (a 'segment') from the buffer in the window.
    Move cursor to line wstart in window.  Display nlines starting at bstart
    in the buffer.  Clip nlines to fit in window if needed.  Pad buffer lines
    with empty lines to reach nlines if needed. Move cursor to line after last.
    """
    nlines = min(nlines, wlines-wstart+1) # clip nlines to fit window
    nblines = min(nlines, len(ed.buffer)-bstart+1) # n of lines from buffer
    nelines = nlines - nblines # number of empty lines at end of window
    display.put_cursor(wstart, 1)
    for line in ed.buffer[bstart:bstart+nblines]:
        display.putstr(line.rstrip('\n')[:tcols+1])
        display.kill_line() # end of buffer line to window edge
        display.next_line()
    for iline in range(nelines+1): # empty lines at end of window
        display.kill_line() # entire line
        display.next_line()

def locate_segment():
    """
    Select segment to put in window, that best positions dot in the window.
    Return buftop, line in current buffer to put at line 1 in window
    """
    if ed.dot < wlines - 1: # dot is near top of buffer, show first page
        return 1
    else: 
        return ed.dot - (wlines // 2) # put dot near center of window

def wline(iline):
    'Return index of line in window that displays iline from buffer'
    wiline = iline - buftop + 1
    return wiline if wiline >=1 else 1

def put_marker(bufline, attribs):
    'On the display, mark first char in line bufline in buffer with attribs'
    line = ed.buffer[bufline] if ed.buffer and 1 <= bufline <= ed.S() else ''
    ch0 = line[0] if line.rstrip('\n') else ' ' # line might be empty or RET 
    display.put_cursor(wline(bufline), 1)
    display.render(ch0, attribs)

def update_status():
    'Update status line at the bottom of the window'
    display.put_cursor(wlines, 1) # window status line
    display.render(ed.status().ljust(tcols)[:tcols+1],display.white_bg)  
    display.put_cursor(tlines, 1) # return cursor to command line

def refresh():
    '(Re)Display buffer segment, marker, status without moving segment'
    update_lines(wlines-1, buftop, 1)
    put_marker(ed.dot, display.white_bg)
    update_status()
    
def recenter():
    'Move buffer segment to put dot in center, display segment, marker, status'
    global buftop
    buftop = locate_segment()
    refresh()

def update_window(new_dot, bstart):
    """
    Move dot to new_dot and update display from bstart to end of window.
    Also move marker and update status line. Page down if needed.
    """
    put_marker(ed.dot, display.clear)
    ed.dot = new_dot # this is all that move_dot(new_dot) does
    if buftop <= ed.dot <= buftop + wlines - 2:
        wstart = bstart - buftop + 1 # dot line in window
        nlines = wlines - wstart # dot to end of window
        update_lines(nlines, bstart, wstart)
        put_marker(ed.dot, display.white_bg)
        update_status()
    else:
        recenter()

# Display functions: show effects of editing commands

# Functions used by editing commands defined in the sked module.
# The default arguments defined in sked produce no display output. 
# These functions, when passed to fcns in sked, do produce display output.
# In this way they are used to define the wrapped display commands below.
# The function here display_<name> is passed to the sked fcn ed.<name>.

def display_move_dot(iline):
    'Display effect of ed move_dot function.  Move current line, dot, to iline'
    put_marker(ed.dot, display.clear)
    ed.dot = iline # this is all that ed.move_dot does
    if buftop <= ed.dot <= buftop + wlines - 2:
        put_marker(ed.dot, display.white_bg)
        update_status()
    else:
        recenter()

def print_nothing(value, sep=' ', end='\n', file=sys.stdout, flush=False):
    """
    Pass to ed cmds printline arg to suppress printing during display.
    Argument declaration must be the same as builtin print.
    """
    return

def display_restore_buffer(bname):
    'Display effect of ed restore_buffer function, fill entire window'
    global buftop
    # This next line does exactly what ed.restore_buffer does
    ed.bufname, ed.filename, ed.buffer, ed.dot, ed.saved = ed.buffers[bname]
    buftop = locate_segment() # buftop: line in buffer at top of window
    update_lines(wlines-1, buftop, 1) # fill window starting at buftop in buffer
    put_marker(ed.dot, display.white_bg)

def display_e(iline):
    'Display effect of ed e(dit) fcn: display new buffer contents around iline'
    ed.dot = iline
    recenter()

def display_set_saved(status):
    'Assign ed.saved and update_status, so saved in status line updates'
    ed.saved = status # this is all that ed.set_saved does
    update_status()

def display_d(iline):
    """
    Display effect of ed d(elete) function, deleting one or more lines.
    Move dot to iline and update dislay from iline+1 to end of window,
    because all lines below the deleted lines must be moved up.
    iline (dot) is the last line before the delete, iline+1 is first line after.
    """
    update_window(iline, iline+1)

def display_y(iline):
    """
    Display effect of ed y(ank) function, appending one or more deleted lines.
    All lines below the appended lines must be moved down.
    iline here is the new dot, the last of the lines appended from yank.
    The first of the lines appended from yank is at iline - len(yank) + 1
    """
    update_window(iline, iline-len(ed.yank)+1)

def display_c(iline):
    """
    Display the effect of the ed c(hange) function, replacing the changed line.
    A call to c() might call this several times, once for each changed line.
    Move dot to iline, redisplay line, mark current line, update the status.
    """
    put_marker(ed.dot, display.clear)
    ed.dot = iline
    display.put_cursor(wline(ed.dot), 1)
    display.putstr(ed.buffer[ed.dot].rstrip('\n')[:tcols+1])
    display.kill_line()
    put_marker(ed.dot, display.white_bg)
    update_status()

# Display functions: append mode for sked a() command

# Enter append mode by typing a() in the REPL.
# Then enter the lines of text in place in the display window.
# Exit append mode by typing . by itself at the start of a line.
# We do not update the status line in append mode, to minimize cursor motion.

# That's how we plan to make it work.
# For now we are still entering text in the REPL - revisions to come

def display_input_line():
    'Call builtin input() and return line'
    return input()

def display_a(iline):
    """
    Display effect of ed a(ppend) function, appending a single line.
    A single call to ed a() might call this several times, once for each line.
    Move dot to iline and update display from dot to end of window,
    because all lines below the appended line must be pushed down.
    Also move marker and update status line. Page down if needed.
    """
    update_window(iline, iline)

# Display functions: editing commands

# Editing functions that generate display output
# by wrapping functions from sked and passing the display fcns defined above.

def e(fname):
    ed.e(fname, display_e)

def b(bname=None):
    ed.b(bname, display_restore_buffer, update_status)

def k():
    ed.k(display_restore_buffer, update_status)

def w(fname=None):
    ed.w(fname, display_set_saved)

def display_p(start=None, end=None):
    ed.p(start, end, print_nothing, display_move_dot)

p = display_p

def l():
    ed.l(display_p)

def rl():
    ed.rl(display_p)

def v(nlines=None):
    ed.v(nlines, display_p)

def rv(nlines=None):
    ed.rv(nlines, display_p, display_move_dot)

def s(target=None, forward=True):
    ed.s(target, forward, print_nothing, display_move_dot)

def r(target=None):
    s(target, forward=False)

def tail(nlines=None):
    ed.tail(nlines, display_p)

def a(iline=None):
    ed.a(iline, display_move_dot, display_input_line, display_a)

def d(start=None, end=None):
    ed.d(start, end, display_d)

def y(iline=None):
    ed.y(iline, display_y)

def c(old=None, new=None, start=None, end=None, count=-1):
    ed.c(old, new, start, end, count, display_c)

# Display functions: window management

def open_frame():
    'Clear display above status line and limit scrolling to the lines below'
    display.put_cursor(wlines, 1) # window status line
    display.erase_above()
    display.set_scroll(flines+1, tlines)

def win(nlines=None):
    """
    Create or resize win(dow) for display at the top of the terminal window.
    Frame size is stored in flines.  First, clear above flines to clear frame.
    If nlines is given, assign to flines.  Smaller nlines enlarges cmd region.
    Set scrolling region to lines below flines.
    Show status line about current buffer at bottom of frame.
    """
    global tlines, tcols, flines, wlines, buftop
    tlines, tcols = terminal_util.dimensions()
    display.put_cursor(flines+1, 1)
    display.erase_above() # clear old window in case new nlines < flines
    if not nlines: nlines = flines
    if nlines > tlines - 2:
        print(f'? {nlines} lines will not fit in terminal of {tlines} lines')
        return
    flines = nlines
    wlines = flines
    ed.pagesize = wlines - 2
    open_frame()
    recenter()

def zen(nlines=None):
    'Alternative to win for a distraction-free writing experience'
    open_frame()
    update_status()

def clr():
    'cl(ea)r window from display by restoring full-screen scrolling'
    display.set_scroll(1, tlines)
    display.put_cursor(tlines, 1) # set_scroll leaves cursor on line 1

