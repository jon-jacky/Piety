"""
breakpt.py

Enable debugging display editors with Pdb while they are running. 

Defines our breakpt function and assigns it to sys.breakpointhook.
After you import this breakpt module, calls to the Python builtin function
breakpoint will call our breakpt function.

Our breakpt function sets the terminal to line mode, moves the cursor from 
the display window to the scrolling REPL region, then calls the builtin
function breakpoint() so you can use Pdb in the REPL region while window
contents remain undisturbed on the display. When you are done with the
debugger, type the Pdb c (continue) command. Then breakpt() returns the
terminal to character mode and puts the cursor at dot in the display
window, so you can resume using the display editor.
In general, the cursor is not at dot when breakpt() is invoked, so when
breakpt() returns it often does not return the cursor to the right place,
and subsequent code does not have the intended effect. The code does not
record the location of the cursor, so this is the best we can do. The
workaround it to invoke refresh(), for example by typing C-l, right after
returning from breakpt() with Pdb c. This puts the correct contents on
the display and restores the cursor to the correct position.

This module and its function are named breakpt to avoid a name clash with
the builtin function breakpoint.
"""

import pdb, sys
import terminal, display
import sked as ed
import edsel as fr
    
def breakpt():
    """
    Run pdb in scrolling REPL region to preserve window contents.
    Use as breakpoint hook.
    """
    x = 42 # local variable to examine with Pdb p
    terminal.set_line_mode() # Prepare for using debugger at breakpoint
    display.put_cursor(fr.tlines, 1) # Put cursor in REPL region for Pdb commands
    pdb.set_trace() # Enter Pdb debugger, use Pdb commands until Pdb c (continue)
    terminal.set_char_mode() # Restore terminal state 
    display.put_cursor(fr.wline(ed.dot), ed.point + 1) # Restore cursor to window

sys.breakpointhook = breakpt     
