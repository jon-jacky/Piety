"""
edie.py - ed + wyshka, ed with command interpreter that also provides python
            but *not* samysh script facility
"""

import ed, wyshka

# add embedded python interpreter - not available running scrips with x command
process_line = wyshka.shell(process_line=ed.process_line,
                            command_mode=(lambda: ed.command_mode),
                            command_prompt=(lambda: ed.prompt))

def startup(*filename, **options):
    ed.startup(*filename, **options)
    wyshka.prompt = ed.prompt

def main(*filename, **options):
    'Top level edo command to invoke from Python REPL or __main__'
    startup(*filename, **options) # defined above, based on ed.startup
    while not ed.quit:
        line = input(wyshka.prompt) # blocks!
        process_line(line)

if __name__ == '__main__':
    filename, options = ed.cmd_options()
    main(*filename, **options)
