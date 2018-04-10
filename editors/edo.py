"""
edo.py - ed + wyshka, ed with command interpreter that also provides python 
            + samysh, run script from buffer with optional echo and delay
"""

import ed, samysh, wyshka

# Define x command so it can also be imported by edsel, eden etc.
# to use with their own do_commands, by calling samysh.add_command.

def x_command(do_command):
    """
    Return function to run script from buffer using do_command, 
    with optional echo and delay.
    """
    def x(paramstring):
        """
        Run script from buffer with optional echo and delay, coded in line arg.
        Named x for eXecute, a single letter like other ed command functions.
        """
        bufname, _, params = paramstring.partition(' ')
        bufname = ed.match_prefix(bufname, ed.buffers)
        if bufname in ed.buffers and bufname != ed.current:
            lines = ed.buffers[bufname].lines[1:] # lines[0] always empty
            samysh.run_script(params, lines, do_command)
        else:
            print('? buffer name')
    return x

# add embedded python interpreter
_do_command = wyshka.shell(do_command=ed.do_command, 
                           command_mode=(lambda: ed.mode == ed.Mode.command),
                           command_prompt=(lambda: ed.prompt))

# add command to run script from buffer with optional echo and delay
do_command = samysh.add_command(x_command(_do_command), _do_command)

def startup(*filename, **options):
    ed.startup(*filename, **options)
    wyshka.prompt = ed.prompt

def edo(*filename, **options):
    'Top level edo command to invoke from Python REPL or __main__'
    startup(*filename, **options) # defined above, based on ed.startup
    while not ed.quit:
        line = input(wyshka.prompt) # blocks!
        do_command(line) # defined above, based on ed.do_command

if __name__ == '__main__':
    filename, options = ed.cmd_options()
    edo(*filename, **options)
