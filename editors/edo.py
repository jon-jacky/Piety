"""
edo.py - ed + wyshka, ed with command interpreter that also provides python 
            + samysh, run script from buffer with optional echo and delay
"""

import ed, samysh, wyshka

# defined here not in samysh because it depends on ed module and ed cmd fmt
def run_script(paramstring, do_command):
    """
    Run script of commands from another buffer with optional echo and delay
     paramstring is usually 'bufname echo delay'
     bufname is not optional, and it cannot be the current buffer.
     echo - optional, default True; delay - optional, default 0.2 sec
    do_command is function to call on command string after applying echo, delay
    """
    params = paramstring.split()
    if params:
        bufname = ed.match_prefix(params[0], ed.buffers)
        if bufname in ed.buffers and bufname != ed.current:
            echo, delay = True, 0.2
            if len(params) > 1:
                echo = params[1] not in ('0','f','false','F','False')
            if len(params) > 2:
                try:
                    delay = float(params[2])
                except ValueError:
                    pass # use default
            # Must define samysh_do... here, echo, delay might differ each call
            _do_command = samysh.show_command(do_command=do_command,
                                              echo=echo, delay=delay)
            for line in ed.buffers[bufname].lines[1:]: # lines[0] always empty
                _do_command(line.rstrip()) # remove terminal \n 
        else:
            print('? buffer name')
    else:
        print('? buffername echo delay')

def add_scripting(name, do_command):
    'Augment do_command with a new command (name) to run script from buffer'
    def _do_command(line):
        line = line.lstrip()
        if ed.command_mode and line.startswith(name):
            run_script(line[1:], do_command) # assumes command name is 1 char
        else:
            do_command(line)
    return _do_command

# add embedded python interpreter
_do_command = wyshka.shell(do_command=ed.do_command, 
                           command_mode=(lambda: ed.command_mode),
                           command_prompt=(lambda: ed.prompt))

# add x command to run script with optional echo and delay
do_command = add_scripting('x', _do_command)

def startup(*filename, **options):
    ed.startup(*filename, **options)
    wyshka.prompt = ed.prompt

def edo(*filename, **options):
    'Top level edo command to invoke from Python REPL or __main__'
    startup(*filename, **options) # startup in this module, based on ed.startup
    while not ed.quit:
        line = input(wyshka.prompt) # blocks!
        do_command(line) # do_command in this module, based on ed.do_command

if __name__ == '__main__':
    filename, options = ed.cmd_options()
    edo(*filename, **options)
