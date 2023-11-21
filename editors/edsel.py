"""
edsel.py - Display editor that uses the same commands as *sked*.

Display buffer contents in a window as they are updated by the sked editor.

See README.md for directions on using edsel, NOTES.txt about its code. 
"""

import sys # skip argument declaration has file=sys.stdout
import terminal_util, display
import sked as ed

# Define and initialize global variables used by this module.
# import the init module only the *first* time this module is imported.
# Then we can reload this module without re-initializing those variables.
try:
    _ = flines # if this variable is defined, then init was already imported
except:
    from edselinit import *

# Display functions: building blocks

def in_window(iline):
    'Return True if buffer index iline is within the window.'
    return (buftop <= iline <= buftop + wlines - 2)

def wline(iline):
    'Return index of line in window that displays iline from buffer.'
    wiline = iline - buftop + 1
    return wiline if wiline >=1 else 1

def locate_segment(iline):
    """
    iline is line in the buffer.
    Select segment to put in window, that best positions iline in the window.
    Return buftop, line in current buffer to put at top line in window
    """
    if iline < wlines - 1: # iline is near top of buffer, show first page
        return 1
    else: 
        return iline - (wlines // 2) # put iline near center of window

def update_lines(bstart, wstart, nlines):
    """
    Display consecutive lines (a 'segment') from the buffer in the window.
    Display nlines, starting at bstart in buffer, starting at wstart in window.
    Clip nlines if needed, to fit in window, and not run past end of buffer.
    Leave cursor after the last line displayed.
    """
    nlines = min(nlines, wintop+wlines-wstart) # n of lines at end of window
    nlines = min(nlines, len(ed.buffer)-bstart+1) # n of lines at e.o. buffer
    display.put_cursor(wstart, 1)
    for line in ed.buffer[bstart:bstart+nlines]:
        display.putstr(line.rstrip('\n')[:tcols])
        display.kill_line() # end of buffer line to window edge
        display.next_line()

def update_window():
    'Update entire window up to status line, starting at line buftop in buffer'
    update_lines(buftop, wintop, wlines-1)

def update_below(bstart, offset=0):
    """
    Update lines in the window starting with (including) buffer line bstart
    down to (but not including) the status line. Accept default offset=0 
    to begin updating at present position of bstart in the window, or
    optionally assign offset to move bstart and following lines down.
    """
    wstart = wline(bstart) + offset
    nlines = wlines - wstart
    update_lines(bstart, wstart, nlines)

def erase_lines(nlines):
    """
    Completely erase nlines lines starting at current cursor position.
    Leave cursor at line after last line erased.
    """
    for iline in range(nlines):
        display.kill_whole_line()
        display.next_line()

def open_line(iline):
    """
    Open line after iline. Put cursor there to prepare for input().
    If text after iline, push it all down one line to make room for new line.
    """
    global buftop
    if not in_window(iline+1):
        display.put_cursor(wintop, 1) # first line of window
        erase_lines(wlines-1) # erase window contents but not status line
        buftop = locate_segment(iline)
        update_window()
    display.put_cursor(wline(iline+1), 1)
    if ed.S() >= iline+1: # more lines after this one in buffer
        display.kill_line() # clear this line to prepare for input()
        update_below(iline + 1, 1) # offset 1 for line we just cleared
        display.put_cursor(wline(iline+1),1) # restore cursor after update_...

def put_marker(bufline, attribs):
    'On the display, mark first char in line bufline in buffer with attribs'
    line = ed.buffer[bufline] if ed.buffer and 1 <= bufline <= ed.S() else ''
    ch0 = line[0] if line.rstrip('\n') else ' ' # line might be empty or RET 
    display.put_cursor(wline(bufline), 1)
    display.render(ch0, attribs)

def restore_cursor_to_cmdline():
    display.put_cursor(tlines, 1)

def update_status():
    'Update status line at the bottom of the window'
    display.put_cursor(wintop+wlines-1, 1) # window status line
    display.render(ed.status().ljust(tcols)[:tcols],display.white_bg)  
    restore_cursor_to_cmdline()

def refresh():
    """
    Refresh the focus window.
    (Re)Display lines from segment, marker, status without moving segment.
    """
    display.put_cursor(wintop, 1) # top line in window
    erase_lines(wlines-1) # erase entire window contents above status line
    update_window() # FIXME did we really have to erase_lines before this?
    put_marker(ed.dot, display.white_bg)
    update_status()
    
def recenter():
    'Move buffer segment to put dot in center, display segment, marker, status'
    global buftop
    buftop = locate_segment(ed.dot)
    refresh()

# Display functions: show effects of editing commands

def display_move_dot(iline):
    'Display effect of ed move_dot function.  Move current line, dot, to iline'
    put_marker(ed.dot, display.clear)
    ed.dot = iline # this is all that ed.move_dot does
    if in_window(ed.dot):
        put_marker(ed.dot, display.white_bg)
        update_status()
    else:
        recenter()

def display_change_lines(start, end):
    'Display effect of ed change_lines fcn. Redraw start to end, move dot.'
    put_marker(ed.dot, display.clear)
    ed.dot = end # this is all that ed.change_lines does
    if in_window(ed.dot):
        update_lines(start, wline(start), end-start+1) # bstart, wstart, nlines
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
    ed.restore_buffer(bname)
    recenter()

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
    iline (dot) is the last line before the delete, iline+1 is first line after.
    Move dot to iline and update display from dot + 1 to end of window,
    because all lines below the deleted lines must be moved up.
    At the end of the buffer, write empty lines at the bottom of the window.
    Also move marker and update status line. Page down if needed.
    """
    put_marker(ed.dot, display.clear)
    ed.dot = iline # this is all that move_dot(iline) does
    if in_window(ed.dot):
        update_below(ed.dot)
        nlines = wlines - wline(ed.dot) # n of lines to end of window
        nblines = ed.S() - (ed.dot + 1) # n of lines to end of buffer
        nelines = nlines - nblines # n of empty lines at end of window
        erase_lines(nelines+1) # sic +1.  make empty lines at end of window.
        put_marker(ed.dot, display.white_bg)
        update_status() 
    else:
        recenter()

def display_y(iline):
    """
    Display effect of ed y(ank) function, appending one or more deleted lines.
    All lines below the appended lines must be moved down.
    iline here is the new dot, the first line after the yanked lines
    (this is actually the same line of text where dot was before yank).
    The first of the lines appended from yank is at iline - len(yank)
    Update the display from there to the end of the window.
    Also move marker and update status line. Page down if needed.
    """
    put_marker(ed.dot, display.clear)
    ed.dot = iline # this is all that move_dot(iline) does
    if in_window(ed.dot):
        update_below(ed.dot - len(ed.killed)) # first yanked line
        put_marker(ed.dot, display.white_bg)
        update_status() 
    else:
        recenter()

def display_c(iline):
    """
    Display the effect of the ed c(hange) function, replacing the changed line.
    A call to c() might call this several times, once for each changed line.
    Move dot to iline, redisplay line, mark current line, update the status.
    """
    put_marker(ed.dot, display.clear)
    ed.dot = iline
    display.put_cursor(wline(ed.dot), 1)
    display.putstr(ed.buffer[ed.dot].rstrip('\n')[:tcols])
    display.kill_line()
    put_marker(ed.dot, display.white_bg)
    update_status()

def display_j(iline):
    'Display effect of ed j(oin lines) function.'
    display.put_cursor(wline(iline), 1)
    display.putstr(ed.buffer[iline].rstrip('\n')[:tcols])
    display_d(iline)

# Display functions: append mode for sked a() command

# Enter append mode by typing a() in the REPL.
# Then enter the lines of text in place in the display window.
# Exit append mode by typing . by itself at the start of a line.
# We do not update the status line in append mode, to minimize cursor motion.

def display_start_a(iline):
    """
    Call once when user types a() in the REPL. Move dot to iline.
    Open line after dot. Put cursor there to prepare for display_input_line.
    If any text after dot, push it all down one line to make room for new line.
    """
    display.put_cursor(wlines, 1) # status line does not update in append mode
    display.render('Appending...'.ljust(tcols)[:tcols],display.white_bg)  
    put_marker(ed.dot, display.clear)
    ed.dot = iline # sked a() does this.  iline might be far from previous dot.
    open_line(ed.dot) # create space, move cursor to prepare for first input()

def display_input_line():
    """
    Call this function when cursor is already on open line, ready for input()
    Call builtin input() and return line that was input.
    input() itself displays the line in the window as it is typed.
    If line is just . by itself, that means exit append mode, close that line.
    This function only updates window when exiting append mode after '.'
    display_a updates window when input() returns a line of text to append.
    """
    line = input() # sked a() does this
    if line == '.': # done with append mode, so close line
        if ed.S() > ed.dot:  # more in the buffer after this line
            update_below(ed.dot + 1)
            if in_window(ed.S()+1): # on the last page, at least one empty line
                display.kill_whole_line() # extra line left by removing '.'
        else: # at the end of the buffer
            display.put_cursor(wline(ed.dot)+1,1)
            display.kill_whole_line() # erase '.'
        put_marker(ed.dot, display.white_bg)
        update_status() # also returns cursor to REPL command line
    return line # caller sked a() tests line, may exit from append mode

def display_a(iline):
    """
    Display effect of ed a(ppend) function, appending a single line.
    A single call to ed a() might call this several times, once for each line.
    Text of line is already on screen at iline, put there by previous input().
    We only call this fcn if input() did *not* return '.',
    so we can advance dot to iline now.
    Move cursor down, open next line to prepare for next input() call.
    """
    put_marker(ed.dot, display.clear)
    ed.dot = ed.dot + 1  # advance dot to line just input(), like sked a()
    open_line(ed.dot) # create space, move cursor to prepare for next input()

# Display functions: editing commands

def e(fname):
    ed.e(fname, display_e)

def b(bname=None):
    ed.b(bname, display_restore_buffer)

def k():
    ed.k(display_restore_buffer)

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
    ed.a(iline, display_start_a, display_input_line, display_a)

def d(start=None, end=None, append=False):
    ed.d(start, end, append, display_d)

def y(iline=None):
    ed.y(iline, display_y)

def c(old=None, new=None, start=None, end=None, count=-1):
    ed.c(old, new, start, end, count, print_nothing, display_c)

def indent(start=None, end=None, nspaces=None, outdent=False):
    ed.indent(start, end, nspaces, outdent, display_change_lines)

def outdent(start=None, end=None, nspaces=None):
    ed.outdent(start, end, nspaces, display_change_lines) 

def wrap(start=None, end=None, lmarg=None, rmarg=None):
    ed.wrap(start, end, lmarg, rmarg, move_dot=display_y)

def j(start=None, end=None):
    ed.j(start, end, move_dot=display_j)

# Display functions: window management

def open_frame():
    """
    Create a 'frame' to contain windows, potentially more than one.
    Clear display above status line and limit scrolling to the lines below.
    """
    display.put_cursor(wlines, 1) # window status line
    display.erase_above()
    display.set_scroll(flines+1, tlines)

def win(nlines=None):
    """
    Create or resize win(dow) for display at the top of the terminal window.
    Frame size is stored in flines.  First, clear above flines to clear frame.
    If nlines is given, assign to flines.  Smaller nlines enlarges cmd region.
    Use of flines and nlines here assumes just one window, maybe revise later.
    Set scrolling region to lines below flines.
    Show status line about current buffer at bottom of frame.
    """
    global tlines, tcols, flines, wlines
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
    ed.rmargin = tcols - 8
    open_frame()
    recenter()

def save_window(wkey):
    """
    Save window items in saved windows at the index wkey.
    wkey is arg so we can save windows other than focus window.
    Save window's buffer also, next window might use a different buffer.
    """
    windows[wkey] = { 'wintop': wintop, 'wlines': wlines, 'buftop': buftop,
                      'bufname': ed.bufname, 'dot': ed.dot } 
    ed.save_buffer() # FIXME? saves current buffer, not buffer for window wkey
                     # BUT wkey is only used in o2 where buffer is the same

def restore_window(wkey):
    """
    Restore saved window items at wkey to the focus window.
    If window uses a different buffer, restore that buffer too.
    """
    global focus, wintop, wlines, buftop # but not bufname, dot, they are in ed
    # default values for missing keys are just the current values
    focus = wkey
    wintop = windows[wkey].get('wintop', wintop)
    wlines = windows[wkey].get('wlines', wlines)
    buftop = windows[wkey].get('buftop', buftop)
    bufname = windows[wkey].get('bufname', ed.bufname) # *local* bufname here!
    if bufname != ed.bufname:
        ed.prev_bufname = ed.bufname
        ed.restore_buffer(bufname) # assign global bufname, buffer, dot etc.
    else:
        ed.dot = windows[wkey].get('dot', ed.dot)

def o2():
    'Split focus window, focus remains in top half, bottom half is new saved'
    global wintop, wlines
    if len(wkeys) >= maxwindows:
        print('? no more windows\r\n', end='')
        return
    # When we split a window, top half remains focus window; keep same wintop.
    prev_wlines = wlines # needed later to size lower window
    wlines = wlines // 2 
    ed.pagesize = wlines - 2
    recenter()  # if dot was in lower half of window, move up. reassign buftop.
    save_window(focus)
    # bottom half
    wkey = (max(wkeys) + 1) % maxwindows  # wkey for new window
    # insert new wkey into wkeys right after focus window entry
    for ikey, _ in enumerate(wkeys):
        if wkeys[ikey] == focus:
            wkeys[ikey+1:ikey+1] = [ wkey ] # insert new wkey after focus entry
            break
    # Calculate new bottom window position, size
    wintop = wintop + wlines
    wlines = prev_wlines - wlines
    recenter() # center dot in this window also, calculate new buftop.
    save_window(wkey)
    restore_window(focus)
    # FIXME? Set cursor to original focus window again?

def o1():
    'Return to single window, make focus window occupy the whole frame.'
    global wintop, wlines, wkeys, windows
    if len(wkeys) <= 1:
        print('? only one window\r\n', end='')
        return
    windows.clear()
    wintop = 1
    wlines = flines
    ed.pagesize = wlines - 2
    recenter() # reassigns buftop
    save_window(focus) # will be overwritten when next time window is split

def on():
    'Next window, move focus to next window below, until wrap around to top'
    global focus
    if len(wkeys) <= 1:
        print('? only one window\r\n', end='')
        return
    save_window(focus) # window contents (buffer and/or dot) may have changed
    for ikey, wkey in enumerate(wkeys):
        if wkeys[ikey] == focus:
            break
    ikey = (ikey + 1) % len(wkeys) # index of next window below, wrap around
    focus = wkeys[ikey]
    restore_window(focus)
    # Window is already visible, we should not have to refresh or recenter it.
    # But we should leave marker in former window and put cursor in new window.

def zen(nlines=None):
    'Alternative to win for a distraction-free writing experience'
    open_frame()
    update_status()

def clr():
    'cl(ea)r window from display by restoring full-screen scrolling'
    display.set_scroll(1, tlines)
    restore_cursor_to_cmdline() # set_scroll leaves cursor on line 1

