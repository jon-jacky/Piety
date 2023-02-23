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

# Functions to patch into sked module

def skip(value, sep=' ', end='\n', file=sys.stdout, flush=False):
    """
    Do nothing, assign to sked.printline to suppress printing during display
    Argument declaration must be the same as builtin print
    """
    return

ed_move_dot = ed.move_dot # save it so we can restore it 

def move_dot(iline):
    'Move current line, dot, to iline'
    ed_move_dot(iline)
    # For now, just update status line with new dot
    display.put_cursor(wlines, 1) # window status line
    display.render(ed.status().ljust(tcols)[:tcols+1],display.white_bg)  
    display.put_cursor(tlines, 1) # return cursor to command line
# At this time there is just one window that fills the frame.

def win(nlines=None):
    """
    Create win(dow) for display editor at the top of the terminal window.
    Default frame size nlines is stored flines, if nlines given replace flines.
    Clear text from frame, set scrolling region to lines below frame.
    Show status line about current buffer at bottom of frame.
    """
    global tlines, tcols, flines, wlines, ed_move_dot
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
    ed_move_dot = ed.move_dot # save latest version so it can be restored
    ed.move_dot = move_dot    # patch sked with version defined above

def cl():
    'cl(ear) away the text editing frame, by restoring full screen scrolling'
    display.set_scroll(1, tlines)
    display.put_cursor(tlines, 1) # set_scroll leaves cursor on line 1
    # Restore patched functions in sked
    ed.printline = print # re-enable printing when no display
    ed.move_dot = ed_move_dot
