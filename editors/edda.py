"""
edda.py - ed + wyshka, ed command interpreter that also provides python 
"""

import ed, wyshka

do_command = wyshka.wyshka(do_command=ed.do_command, 
                           command_mode=(lambda: ed.command_mode),
                           command_prompt=(lambda: ed.prompt))

if __name__ == '__main__':
    filename, options = ed.cmd_options()
    ed.startup(*filename, **options)
    ed.main(do_command=do_command, prompt=(lambda: wyshka.prompt))
