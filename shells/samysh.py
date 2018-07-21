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

def run_script(paramstring, commands, do_command):
    """
    Run script of commands with optional echo and delay
     commands can be any sequence: list of lines or keycodes, string of chars
     paramstring is usually 'echo delay'
     echo - optional, default True; delay - optional, default 0.2 sec
     do_command is fcn to call on command after applying echo, delay
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
    for command in commands:
        _do_command(command.rstrip()) # remove terminal \n if there is one

def add_command(command, do_command):
    """
    Return a function that augments do_command with a new command.
    The new command is a function with a single string argument, that
    contains all its parameters.  A command line for the new command
    starts with the command name, which must be the same as the name
    of the command function.  The rest of the command line is the
    string of parameters that is passed to the command function.  Any
    command lines that do not start with the new command name are
    passed on to do_command.   The command line cannot begin with line
    addresses preceding the command name, as in classic ed commands.
    The command name can be more than one character, unlike in classic ed.

    After executing the new command, go on and execute do_command. 
    So the new command should be coded with a guard, and its body should
    do nothing if its guard fails.  The guard should be strong enough
    so that none of the cases in do_command runs if the guard succeeds.
    """
    def _do_command(line):
        line = line.lstrip()
        if line.startswith(command.__name__):
            _, _, paramstring = line.partition(command.__name__)
            command(paramstring.lstrip())
        # Always execute do_command after command
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
