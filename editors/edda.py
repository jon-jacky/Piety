"""
edda.py - Defines the ed Console job that wraps the ed.py line editor,
  along with the wyshka enhanced Python shell and samysh script execution.
  Contrast to the ed.py main function and etty.py.
"""

import edo, wyshka, console

ed = console.Console(prompt=(lambda: wyshka.prompt), 
                     do_command=edo.wyshka_do_command,
                     stopped=(lambda command: edo.ed.quit),
                     keymap=(lambda: (console.command_keymap 
                                      if edo.ed.command_mode 
                                      else console.insert_keymap)),
                     startup=edo.startup, cleanup=edo.ed.q)

def edda(*filename, **options):
    ed.run(*filename, **options)

if __name__ == '__main__':
    filename, options = edo.ed.cmd_options()
    edda(*filename, **options)
