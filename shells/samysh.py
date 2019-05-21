"""
samysh.py - Execute command with optional echo and delay.
            Run script, execute each command with optional echo and delay.
            Useful for observing the execution of test scripts.
"""

import time # for blocking time.sleep(), FIXME write nonblocking piety.sleep()

def params(paramstring):
            """
            Get echo and delay parameters used by show_command and run_script.
            Also get buffer name used by edo X_command which uses run_script.
            paramstring has bufname, echo, delay, for example 'modes.ed 0 1'
            Defaults are bufname '', echo True, delay 1 sec.
            """
            bufname, echo, delay = '', True, 1
            params = paramstring.split()
            if len(params) > 0:
                bufname = params[0]
            if len(params) > 1:
                echo = (False if params[1] in ('0','f','false','F','False')
                        else True)
            if len(params) > 2:
                try:
                    delay = float(params[2])
                except ValueError:
                    pass # use default
            return bufname, echo, delay

def show_command(do_command=(lambda line: None), echo=True, delay=None):
    """
    Return a function with one argument (a string, the command line) that
     executes a command with optional echo and delay.
    This function has three optional keyword arguments with defaults:
    do_command is a callable with one string argument - the command line -
     that executes an application command.  Default does nothing.
    echo - Boolean, default True, print each line before executing it.
     To suppress command echo, pass False.
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

def run_script(do_command, commands, echo=True, delay=1.0):
    """
    Run script of commands with optional echo and delay of each command
     commands can be any sequence: list of lines or keycodes, string of chars
     do_command executes a single command: a line of text, a keycode, a char...
     delay is in units of seconds, can be a fraction of a second.
    """
    # Must define _do_command here, echo and delay might differ on each call.
    _do_command = show_command(do_command=do_command,
                               echo=echo, delay=delay)
    for command in commands:
        _do_command(command.rstrip('\n')) # remove terminal \n from line

# run_script takes do_command as an argument.  Therefore run_script cannot
# be included in any program's do_command, it must be added to all the
# cascaded do_commands last, at top level.  Use add_command for this.
# edo.py is an example that uses both run_script and add_command.

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
    """
    def _do_command(line):
        if line.startswith(command.__name__):
            _, _, paramstring = line.partition(command.__name__)
            command(paramstring.lstrip())
        else:
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
