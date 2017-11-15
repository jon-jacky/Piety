"""
edda.py - Run *edo.py* line editor including *wyshka* enhanced shell
  and *samysh* script execution.  Use *console* module instead of
  Python builtin *input()* to collect and edit input lines.  Contrast
  to *ed.py* *main* function and *etty.py*.
"""

import edo, wyshka, console as con

# FIXME? ed = edo.ed  # so we can call ed API without edo. prefix

console = con.Console(prompt=(lambda: wyshka.prompt), 
                      do_command=edo.do_command,
                      stopped=(lambda command: edo.ed.quit),
                      command_keymap=(lambda: (con.command_keymap 
                                               if edo.ed.command_mode 
                                               else con.insert_keymap)))

def main():
    edo.ed.quit = False
    console.run()

if __name__ == '__main__':
    filename, options = edo.ed.cmd_options()
    edo.ed.startup(*filename, **options)
    main()

