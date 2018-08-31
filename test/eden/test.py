"""
test.py - This module contains scripts for several tests.  

Run the tests from the eden command line.  Type eden commands to load
a file of sample text and position the cursor, then type Python
commands to import this module and run one of its scripts.  Prefix the
Python commands with !  For example:

    :E lines20.txt
    :10
    :!import test
    :!test.test(test.dnupdn)

The test function switches from eden command mode to display mode and
then runs the named script.  After the test finishes, type ^Z to exit
from display mode and return to command mode.  Then you can type a
Python command to run another test.
"""

import eden, samysh
from keyboard import * # ^N ^P keycodes, and all the others

# scripts

dnupdn = 3*C_n + 6*C_p +3*C_n  # just a string, all keycodes are single chars

def test(script):
    eden.base_do_command('C')
    samysh.run_script(eden.eden.handle_key, script, echo=(lambda: False))
