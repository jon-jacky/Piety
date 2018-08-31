"""
dnupdn.py - Test eden: run the cursor down, then up, then down with ^N and ^P

Run the test from the eden command line. Type the Python command to
import this module, using the ! prefix:

    :!import dnupdn

After the test finishes, type ^Z to exit from display mode and return
to command mode.

To run the test again in the same session, call this module's main function:

    :!dnupdn.main()
"""

import eden, ed, samysh
from keyboard import * # ^N ^P keycodes, and all the others

keycodes = 3*C_n + 6*C_p +3*C_n  # just a string, all keycodes are single chars

# define a function so we can call it many times
def main():
    ed.E('lines20.txt')
    ed.l(10)
    eden.base_do_command('C')
    samysh.run_script(eden.eden.handle_key, keycodes, echo=(lambda: False))

# so we don't have to call main after initial import
main()
