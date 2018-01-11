"""
edda.py - Run *edo.py* line editor including *wyshka* enhanced shell
  and *samysh* script execution.  Use *console* module instead of
  Python builtin *input()* to collect and edit input lines.  Contrast
  to *ed.py* *main* function and *etty.py*.
"""

import edo, wyshka, console as con

ed = edo.ed  # so we can call ed API without edo. prefix

console = con.Console(prompt=(lambda: wyshka.prompt), 
                      do_command=edo.do_command,
                      stopped=(lambda command: ed.quit),
                      keymap=(lambda: (con.command_keymap 
                                       if ed.command_mode 
                                       else con.insert_keymap)))

def main():
    ed.quit = False
    console.run()

if __name__ == '__main__':
    filename, options = ed.cmd_options()
    ed.startup(*filename, **options)
    main()
