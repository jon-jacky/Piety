"""
frame.py - Frame Editor - display buffer contents in a 'frame' of windows
          as they are updated by commands in the sked line editor.
"""

import sys # skip argument declaration has file=sys.stdout
import terminal_util, display
import sked as ed

# Define and initialize global variables used by fred display functions.
# Conditinally exec only the *first* time this module is imported in a session.
# Then we can reload this module without re-initializing those variables.
try:
    _ = flines # if flines is already defined, then fredinit was already exec'd
except:
    exec(open("frameinit.py").read())

# Display functions that replace ('patch') functions in the sked module

def skip(value, sep=' ', end='\n', file=sys.stdout, flush=False):
    """
    Do nothing, assign to sked.printline to suppress printing during display
    Argument declaration must be the same as builtin print
    """
    return

def update_status():
    'Update status line at the bottom of the window'
    display.put_cursor(wlines, 1) # window status line
    display.render(ed.status().ljust(tcols)[:tcols+1],display.white_bg)  
    display.put_cursor(tlines, 1) # return cursor to command line

_move_dot = ed.move_dot # save it so we can restore it 

def move_dot(iline):
    'Move current line, dot, to iline'
    _move_dot(iline)
    update_status() # for now, just update status line with new dot

_restore_buffer = ed.restore_buffer

def restore_buffer(bname):
    _restore_buffer(bname)
    update_status()
 
# At this time there is just one window that fills the frame.

def win(nlines=None):
    """
    Create win(dow) for display editor at the top of the terminal window.
    Default frame size nlines is stored flines, if nlines given replace flines.
    Clear text from frame, set scrolling region to lines below frame.
    Show status line about current buffer at bottom of frame.
    """
    global tlines, tcols, flines, wlines, _move_dot
    if not nlines: nlines = flines
    tlines, tcols = terminal_util.dimensions()
    if nlines > tlines - 2:
        print(f'? {nlines} lines will not fit in terminal of {tlines} lines')
        return
    flines = nlines
    display.put_cursor(wlines, 1) # window status line
    display.erase_above()
    display.render(ed.status().ljust(tcols)[:tcols+1], display.white_bg)   
    display.set_scroll(flines+1, tlines)
    display.put_cursor(tlines, 1)
    # Patch functions in sked
    ed.printline = skip # suppress printing during display
    _move_dot = ed.move_dot # save latest version so it can be restored
    ed.move_dot = move_dot    # patch sked with version defined above
    _restore_buffer = ed.restore_buffer
    ed.restore_buffer = restore_buffer

def cl():
    'cl(ear) away the text editing frame, by restoring full screen scrolling'
    display.set_scroll(1, tlines)
    display.put_cursor(tlines, 1) # set_scroll leaves cursor on line 1
    # Restore patched functions in sked
    ed.printline = print # re-enable printing when no display
    ed.move_dot = _move_dot
    ed.restore_buffer = _restore_buffer
