"""
samysh.py - Execute command with optional echo and delay.
            Useful for observing the execution of test scripts.
"""

import time # for blocking time.sleep(), FIXME write nonblocking piety.sleep()

def samysh(do_command=(lambda line: None), echo=True, delay=None):
    """
    Return a function with one argument (a string, the command line) that
    executes a command with optional echo and delay.

    This function has three optional keyword arguments with defaults:

    do_command is a callable with one string argument - the command line -
    that executes an application command.  Default does nothing.
     
    echo - if True, print each line before executing it.  Default False.

    delay - seconds to wait after executing line (float, can be < 1.0).
    Default no delay.
    """
    def _do_command(line):
        if echo: 
            print(line)
        do_command(line) 
        if delay and delay > 0:
            time.sleep(delay) # FIXME replace with non-blocking piety.sleep()
    return _do_command

# Test

def execute(line):
    print('Executing %s ...' % line)

do_command = samysh(do_command=execute, echo=True, delay=2.0)

def main():
    while True:
        line = input(':')
        do_command(line)
        if line == 'q':
            return

# Test by reading from script file to demonstrate delay:
# python3 -i -m samysh < lines.txt

if __name__ == '__main__':
    main()
