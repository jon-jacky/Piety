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

# Add command to run script from buffer with optional echo and delay.
_do_command = samysh.add_command(x_command(ed.do_command), ed.do_command)

# Keep new do_command with new x_command separate from ed.add_line
def _process_line(line):
    'process one line without blocking, according to mode'
    if ed.command_mode:
        _do_command(line)
    else:
        ed.add_line(line)

# add embedded python interpreter
process_line = wyshka.shell(process_line=_process_line,
                            command_mode=(lambda: ed.command_mode),
                            command_prompt=(lambda: ed.prompt))

def startup(*filename, **options):
    ed.startup(*filename, **options)
    wyshka.prompt = ed.prompt

def edo(*filename, **options):
    'Top level edo command to invoke from Python REPL or __main__'
    startup(*filename, **options) # defined above, based on ed.startup
    while not ed.quit:
        line = input(wyshka.prompt) # blocks!
        process_line(line)

if __name__ == '__main__':
    filename, options = ed.cmd_options()
    edo(*filename, **options)
