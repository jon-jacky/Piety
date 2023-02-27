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

# Display functions

def open_frame():
    'Clear display above status line and limit scrolling to the lines below'
    display.put_cursor(wlines, 1) # window status line
    display.erase_above()
    display.set_scroll(flines+1, tlines)

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
    for iline in range(nelines): # empty lines at end of window
        display.kill_line() # entire line
        display.next_line()

def update_status():
    'Update status line at the bottom of the window'
    display.put_cursor(wlines, 1) # window status line
    display.render(ed.status().ljust(tcols)[:tcols+1],display.white_bg)  
    display.put_cursor(tlines, 1) # return cursor to command line

# Display editor commands that wrap and replace ('patch') editing cmds in sked

def skip(value, sep=' ', end='\n', file=sys.stdout, flush=False):
    """
    Do nothing, assign to sked.printline to suppress printing during display
    Argument declaration must be the same as builtin print
    """
    return

_move_dot = ed.move_dot # save it so we can restore it 

def move_dot(iline):
    'Move current line, dot, to iline'
    _move_dot(iline)
    update_status() # for now, just update status line with new dot

_restore_buffer = ed.restore_buffer

def restore_buffer(bname):
    _restore_buffer(bname)
    update_status()
 
_e = ed.e

# Name wrapped fcn eW to distinguish from sked e after from sked/frame import *
def eW(fname):
    _e(fname)
    update_status()

# Turn display editing on and off.  Show, clear display editing frame.

def enable_display():
    'Replace ("patch") functions in sked with wrapped display editing fcns'
    global _move_dot, _restore_buffer
    ed.printline = skip # suppress printing during display
    _move_dot = ed.move_dot # save latest version so it can be restored
    ed.move_dot = move_dot    # patch sked with version defined above
    _restore_buffer = ed.restore_buffer
    ed.restore_buffer = restore_buffer
    _e = ed.e
    ed.e = eW

def disable_display():
    'Re-replace patched fcns in sked with original fcns without display'
    ed.printline = print # re-enable printing when no display
    ed.move_dot = _move_dot
    ed.restore_buffer = _restore_buffer
    ed.e = _e

def win(nlines=None):
    """
    Create win(dow) for display editor at the top of the terminal window.
    Default frame size nlines is stored flines, if nlines given replace flines.
    Enable display by replacing ('patching) fcns in sked with wrappers here
    Clear text from frame, set scrolling region to lines below frame.
    Show status line about current buffer at bottom of frame.
    """
    global tlines, tcols, flines, wlines
    if not nlines: nlines = flines
    tlines, tcols = terminal_util.dimensions()
    if nlines > tlines - 2:
        print(f'? {nlines} lines will not fit in terminal of {tlines} lines')
        return
    flines = nlines
    wlines = flines
    enable_display()
    open_frame()
    update_status()

def zen():
    'Alternative to win() for a distraction-free writing experience'
    open_frame()
    update_status()

def clr():
    """
    cl(ear) away display frame by restoring full screen scrolling.
    Restore patched functions in sked to original no-display versions
    """
    disable_display()
    display.set_scroll(1, tlines)
    display.put_cursor(tlines, 1) # set_scroll leaves cursor on line 1
