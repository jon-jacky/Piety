"""
test.py - This module contains scripts for several tests.  

Run the tests from the eden command line.  Type eden commands to load
a file of sample text and position the cursor, then type Python
commands to import this module and run one of its scripts.  Prefix the
Python commands with !  For example:

    :E lines20.txt
    :10
    :!import test
    :!test.run(test.dnupdn)

The test.run function switches from eden command mode to display mode,
runs the named test script, and then returns to command mode and
prints a prompt. Then you can type the ed command ,d to empty the
buffer and clear the window, and type a Python command to run another
script.

When running scripts, the default delay between simulated keystrokes
is 0.2 seconds.  You can override this by including an optional
keyword argument:

    :!test.run(test.dnupdn, delay=0.5)

Some tests do not require any preliminaries, and can be run in a new empty buffer.
See comments before each test case.
"""

import eden, samysh
from keyboard import * # ^A ^B ... keycodes

# This script is just a string, all keycodes are single chars ^N ^P
# First load several lines of text, for example :E lines20.txt
#  then position cursor, for example :10
dnupdn = 3*C_n + 6*C_p +3*C_n  

# This script is a tuple of strings, all keycodes are multiple characters
dnupdn_arrows = 3*(down,) + 6*(up,) + 3*(down,)

# Line editing keycodes in console.Console: ^A ^B ^D ^E ^F ^K ^L ^U bs
# Self-contained, no preliminaries needed
# This script is just a string
inline = ('Here is a line of text' + C_a + 10*C_f + 'new ' + C_e + 4*bs +
          'characters' + 22*C_b + 4*C_d + C_k + 'word' + C_l + ' and stuff' + 
          C_u + 'Start over')

# This script is a tuple of strings, including many single-character keycodes
inline_arrows = (tuple('Here is a line of text',) + (C_a,) + 10*(right,) + 
                 tuple('new ') +
                 (C_e,) + 4*(bs,) + tuple('characters') + 22*(left,) + 4*(C_d,) + 
                 (C_k,) + tuple('word') + (C_l,) + tuple(' and stuff') + (C_u,) +
                 tuple('Start over'))

# Page down, page up in eden.Console: ^V, ^R
# First load several pages of text, for example  :E lines120.txt
#  then position cursor at top for example :1
pgdnup = 8*C_v + 8*C_r

# Enter text, navigate around: cr bs ^P ^N ^A ^F ^B.  Self-contained.  A string.
lines = ('line 1' + cr +
         'line 2' + cr +
         'line 3' + cr +
         'line 4' + cr +
         'line 5' + cr +
         6*C_p + 6*C_n + 3*C_p + 
         'line 2a' + cr + 
         2*C_p + bs + C_a + bs + C_a + bs +
         6*C_f + cr + 
         'line 1a' + cr +
         3*C_f + 4*C_n + 2*C_b + 7*C_p + 
         10*C_f + 6*C_n + 10*C_b + 7*C_p)

# Enter text, navigate around: cr bs ^P ^N ^A ^F ^B.  Self-contained. 
# Tuple of strings
lines_arrows = (tuple('line 1' + cr) +
         tuple('line 2' + cr) +
         tuple('line 3' + cr) +
         tuple('line 4' + cr) +
         tuple('line 5' + cr) +
         6*(up,) + 6*(down,) + 3*(up,) + 
         tuple('line 2a' + cr) + 
         2*(up,) + (bs,) + (C_a,) + (bs,) + (C_a,) + (bs,) +
         6*(right,) + (cr,) + 
         tuple('line 1a' + cr) +
         3*(right,) + 4*(down,) + 2*(left,) + 7*(up,) + 
         10*(right,) + 6*(down,) + 10*(left,) + 7*(up,))

# Delete backwards until join lines, self-contained
del_join = ('line 1' + cr +
            'line 2' + cr +
            'line 3' + cr +
            'line 4' + cr +
            'line 5' + 
            C_a +2*C_p + 3*C_f + 18*bs)

# Delete forwards until join lines, self-contained
del_join_down = ('line 1' + cr +
            'line 2' + cr +
            'line 3' + cr +
            'line 4' + cr +
            'line 5' + 
            C_a +4*C_p + 3*C_f + 18*C_d)


# Set mark, exchange mark and point, cut, paste (yank)
# First load some text, for example, :E lines20.txt
#  then place cursor on first line, :1
# Show that after yank, mark is always the first line of yanked region.
# mark lines 1, move to line 5, cut, yank, move down 5 lines, yank again,
# move down five more lines, yank again.
yank = (C_at + 4*C_n +
        C_x + C_x + 
        C_w +
        C_y +
        C_x + C_x + 
        5*C_n + 
        C_y +
        C_x + C_x +
        5*C_n + 
        C_y +
        C_x + C_x)

def run(script, delay=0.2): # seconds
    eden.base_do_command('C')
    samysh.run_script(eden.eden.handle_key, script, echo=(lambda: False), 
                      delay=delay)
    eden.eden.command_mode()
