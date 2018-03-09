"""
edo.py - ed + wyshka, ed with command interpreter that also provides python 
            + samysh, run script from buffer with optional echo and delay
"""

import ed, samysh, wyshka

# x defined here not in samysh because it depends on ed module and ed cmd fmt
def x(paramstring, do_command):
    """
    Execute script of commands from another buffer with optional echo and delay
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
            _do_command = samysh.samysh(do_command=do_command,
                                        echo=echo, delay=delay)
            for line in ed.buffers[bufname].lines[1:]: # lines[0] always empty
                _do_command(line.rstrip()) # remove terminal \n 
        else:
            print('? buffer name')
    else:
        print('? buffername echo delay')

def mk_x_do_command(do_command):
    'Augment do_command with x command to execute script from buffer'
    def _do_command(line):
        line = line.lstrip()
        if ed.command_mode and line.startswith('x'):
            x(line[1:], do_command)
        else:
            do_command(line)
    return _do_command

## Below here might be the model for the boilerplate parts of edsel, eden etc.

# wyshka adds embedded python interpreter to ed.do_command
_do_command = wyshka.wyshka(do_command=ed.do_command, 
                            command_mode=(lambda: ed.command_mode),
                            command_prompt=(lambda: ed.prompt))

# x_do_command adds x execute script command to _do_command
do_command = mk_x_do_command(_do_command)

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
