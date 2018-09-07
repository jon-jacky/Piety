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
runs the named test script, and then returns to command mode and prints a
prompt.  Then you can type a Python command to run another script.

When running scripts, the default delay between simulated keystrokes
is 0.2 seconds.  You can override this by including an optional
keyword argument:

    :!test.run(test.dnupdn, delay=0.5)
"""

import eden, samysh
from keyboard import * # ^A ^B ... keycodes

# The following scripts are just strings, all keycodes are single chars

# Down, up cursor movement ^N ^P
dnupdn = 3*C_n + 6*C_p +3*C_n  

# Line editing keycodes in console.Console: ^A ^B ^D ^E ^F ^K ^L ^U bs delete
inline = ('Here is a line of text' + C_a + 10*C_f + 'new ' + C_e + 4*bs +
          'characters' + 22*C_b + 4*C_d + C_k + 'word' + C_l + ' and stuff' + 
          C_u + 'Start over')

def run(script, delay=0.2): # seconds
    eden.base_do_command('C')
    samysh.run_script(eden.eden.handle_key, script, echo=(lambda: False), 
                      delay=delay)
    eden.eden.command_mode()
