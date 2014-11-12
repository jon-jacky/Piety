"""
edd configuration that imports Piety console module 
instead of using built-in Python raw_input to get command line.
BUT does not use Piety scheduler.

This is like test/console/test_console_blocking
but also passes in edd.cmd instead of using default echoline command

$ python edd.c
... edd commands
q
$

"""

import edd
import console
import terminal

c0 = console.Console(prompt='', command=edd.cmd, exiter=edd.ed.q) 

console.focus = c0

def main():
    """ 
    loop calling getchar until line terminator, then print buffer contents
    """
    # restart and restore are done by console do_command also
    # BUT both initial c0.restart and final terminal.restore needed here
    c0.restart() # includes terminal.setup()
    edd.init_display()
    key = None # anything but 'q'
    edd.ed.quit = False # allow restart
    while not edd.ed.quit:
        key = c0.getchar() # also updates c0.cmdline
    edd.restore_display()
    terminal.restore() # restore terminal mode

if __name__ == '__main__':
    main()

  
