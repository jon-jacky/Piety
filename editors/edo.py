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
            # do_command passed to samysh is defined below, includes wyshka
            samysh_do_command = samysh.samysh(do_command=do_command,
                                              echo=echo, delay=delay)
            for line in ed.buffers[bufname].lines[1:]: # lines[0] always empty
                samysh_do_command(line.rstrip()) # remove terminal \n 
        else:
            print('? buffer name')
    else:
        print('? buffername echo delay')

def do_command_x(line):
    'Augment ed.do_command with one more command: x execute script from buffer'
    if ed.command_mode and line.lstrip().startswith('x'):
        x(line.lstrip()[1:])
    else:
        ed.do_command(line)

do_command = wyshka.wyshka(do_command=do_command_x, 
                           command_mode=(lambda: ed.command_mode),
                           command_prompt=(lambda: ed.prompt))

def startup(*filename, **options):
    ed.startup(*filename, **options)
    wyshka.prompt = ed.prompt

def main(*filename, **options):
    startup(*filename, **options)
    ed.main(do_command=do_command, prompt=(lambda: wyshka.prompt))

if __name__ == '__main__':
    filename, options = ed.cmd_options()
    main(*filename, **options)
