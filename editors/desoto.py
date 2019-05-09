"""
desoto.py - Defines the edsel Console job that wraps the edsel.py
  display editor, along with the wyshka enhanced Python shell and
  samysh script execution.  Contrast to the edsel.py main function.
"""

import edsel as editor, wyshka, console

ed = editor.edo.ed   # use ed and frame APIs without prefix
frame = editor.frame 

edsel = console.Console(prompt=(lambda: wyshka.prompt),
                        process_line=editor.process_line,
                        stopped=(lambda command: ed.quit),
                        startup=editor.startup, cleanup=editor.cleanup)

edsel.keymap = (lambda: (edsel.command_keymap
                         if ed.command_mode
                         else edsel.input_keymap))

def main(*filename, **options):
    edsel.run(*filename, **options)

if __name__ == '__main__':
    filename, options = ed.cmd_options()
    main(*filename, **options)
