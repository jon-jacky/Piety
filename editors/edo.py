"""
edo.py - ed + wyshka, ed with command interpreter that also provides python 
            + samysh, run script from buffer with optional echo and delay
"""

import ed, samysh, wyshka

def x(paramstring):
    """
    Execute script of commands from another buffer
     paramstring is usually 'bufname echo delay'
     bufname is not optional, and it cannot be the current buffer.
     echo - optional, default True; delay - optional, default 0.2 sec
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
            # wyshka_do_command passed to samysh is defined below
            samysh_do_command = samysh.samysh(do_command=wyshka_do_command,
                                              echo=echo, delay=delay)
            for line in ed.buffers[bufname].lines[1:]: # lines[0] always empty
                samysh_do_command(line.rstrip()) # remove terminal \n 
        else:
            print('? buffer name')
    else:
        print('? buffername echo delay')

def x_do_command(line):
    'Augment ed.do_command with one more command: x execute script from buffer'
    line = line.lstrip()
    if ed.command_mode and line.startswith('x'):
        x(line[1:])
    else:
        ed._do_command(line)

wyshka_do_command = wyshka.wyshka(do_command=x_do_command, 
                                  command_mode=(lambda: ed.command_mode),
                                  command_prompt=(lambda: ed.prompt))

ed.do_command = wyshka_do_command
ed.prompt_thunk = (lambda: wyshka.prompt)

def startup(*filename, **options):
    ed.startup(*filename, **options)
    wyshka.prompt = ed.prompt

def edo(*filename, **options):
    startup(*filename, **options)
    ed.loop()

if __name__ == '__main__':
    filename, options = ed.cmd_options()
    edo(*filename, **options)
