"""
desoto.py - Defines the edda Console job that wraps the edda.py
  display editor, along with the wyshka enhanced Python shell and
  samysh script execution.  Contrast to the edda.py main function.
"""

import edda as editor, wyshka, console

ed = editor.edo.ed   # use ed and frame APIs without prefix
frame = editor.frame

edda = console.Console(prompt=(lambda: wyshka.prompt),
                        process_line=editor.process_line,
                        stopped=(lambda command: ed.quit),
                        startup=editor.startup, cleanup=editor.cleanup)

edda.keymap = (lambda: (edda.command_keymap
                         if ed.command_mode
                         else edda.input_keymap))

def main(*filename, **options):
    edda.run(*filename, **options)

if __name__ == '__main__':
    filename, options = ed.cmd_options()
    main(*filename, **options)
