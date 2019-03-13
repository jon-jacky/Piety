"""
desoto.py - Defines the edsel Console job that wraps the edsel.py
  display editor, along with the wyshka enhanced Python shell and
  samysh script execution.  Contrast to the edsel.py main function.
"""

import edsel as editor, wyshka, console as con

ed = editor.edo.ed  # so we can call ed API without editor.edo. prefix

edsel = con.Console(prompt=(lambda: wyshka.prompt), 
                    process_line=editor.process_line,
                    stopped=(lambda command: ed.quit),
                    startup=editor.startup, cleanup=editor.cleanup)

edsel.keymap = (lambda: (edsel.command_keymap 
                         if ed.command_mode
                         else edsel.input_keymap))

if __name__ == '__main__':
    filename, options = ed.cmd_options()
    edsel.run(*filename, **options)
