"""
desoto.py - Defines the edsel Console job that wraps the edsel.py
  display editor, along with the wyshka enhanced Python shell and
  samysh script execution.  Contrast to the edsel.py main function.
"""

import edsel as editor, wyshka, console as con

ed = editor.edo.ed  # so we can call ed API without editor.edo. prefix

edsel = con.Console(prompt=(lambda: wyshka.prompt), 
                      do_command=editor.do_command,
                      stopped=(lambda command: ed.quit),
                      startup=editor.startup, cleanup=editor.cleanup)

edsel.keymap = keymap=(lambda: (edsel.command_keymap 
                                if ed.command_mode 
                                else edsel.insert_keymap))

def desoto(*filename, **options):
    edsel.run(*filename, **options)

if __name__ == '__main__':
    filename, options = ed.cmd_options()
    desoto(*filename, **options)
