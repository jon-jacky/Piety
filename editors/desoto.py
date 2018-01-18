"""
desoto.py - Run *edsel.py* display editor including *wyshka* enhanced shell
  and *samysh* script execution.  Use *console* module instead of
  Python builtin *input()* to collect and edit input lines.  Contrast
  to *edsel.py* *main* function.
"""

import edsel as editor, wyshka, console as con

ed = editor.edo.ed  # so we can call ed API without editor.edo. prefix

edsel = con.Console(prompt=(lambda: wyshka.prompt), 
                      do_command=editor.do_command,
                      stopped=(lambda command: ed.quit),
                      keymap=(lambda: (con.command_keymap 
                                       if ed.command_mode 
                                       else con.insert_keymap)),
                      startup=editor.startup, cleanup=editor.cleanup)

def main(*filename,**options):
    ed.quit = False
    edsel.run() # FIXME - ignores filename, options for now

def resume():
    main() # no filename, no options - do not disturb present state.

if __name__ == '__main__':
    filename, options = ed.cmd_options()
    main(*filename, **options)
