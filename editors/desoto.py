"""
desoto.py - Run *edsel.py* display editor including *wyshka* enhanced shell
  and *samysh* script execution.  Use *console* module instead of
  Python builtin *input()* to collect and edit input lines.  Contrast
  to *edsel.py* *main* function.
"""

import edsel, wyshka, console as con

ed = edsel.edo.ed  # so we can call ed API without edsel.edo. prefix

console = con.Console(prompt=(lambda: wyshka.prompt), 
                      do_command=edsel.do_command,
                      stopped=(lambda command: ed.quit),
                      keymap=(lambda: (con.command_keymap 
                                       if ed.command_mode 
                                       else con.insert_keymap)),
                      startup=edsel.startup,
                      cleanup=edsel.cleanup)

def main(*filename,**options):
    ed.quit = False
    console.run() # FIXME - ignores filename, options for now

def resume():
    main() # no filename, no options - do not disturb present state.

if __name__ == '__main__':
    filename, options = ed.cmd_options()
    main(*filename, **options)
