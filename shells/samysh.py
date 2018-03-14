"""
samysh.py - Execute command with optional echo and delay.
            Run script, execute each command with optional echo and delay.
            Useful for observing the execution of test scripts.
"""

import time # for blocking time.sleep(), FIXME write nonblocking piety.sleep()

def show_command(do_command=(lambda line: None), echo=True, delay=None):
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

def run_script(paramstring, lines, do_command):
    """
    Run script of commands from another buffer with optional echo and delay
     paramstring is usually 'bufname echo delay'
     echo - optional, default True; delay - optional, default 0.2 sec
     do_command is fcn to call on command string after applying echo, delay
    """
    params = paramstring.split()
    echo, delay = True, 0.2
    if len(params) > 0:
        echo = params[0] not in ('0','f','false','F','False')
    if len(params) > 1:
        try:
            delay = float(params[1])
        except ValueError:
            pass # use default
    # Must define show_command here, echo and delay might differ on each call.
    _do_command = show_command(do_command=do_command,
                               echo=echo, delay=delay)
    for line in lines:
        _do_command(line.rstrip()) # remove terminal \n 


def add_command(new_command, do_command):
    """
    Augment do_command with new_command.  
    When new_command returns False, run do_command.
    """
    def _do_command(line):
        attempted = new_command(line)
        if not attempted:
            do_command(line)
    return _do_command

# Test

def execute(line):
    print('Executing %s ...' % line)

do_command = show_command(do_command=execute, echo=True, delay=2.0)

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
