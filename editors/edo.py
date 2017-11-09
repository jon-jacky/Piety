"""
edo.py - Run *ed.py* line editor.  Use *console* module
  instead of Python builtin *input()* to collect and edit
  input lines.  Contrast to *ed.py* *main* function and *etty.py*.
"""

import ed, console as con

console = con.Console(prompt=(lambda: ed.prompt), 
                      do_command=ed.do_command,
                      stopped=(lambda command: ed.quit),
                      command_keymap=(lambda: (con.command_keymap 
                                               if ed.command_mode 
                                               else con.insert_keymap)))

def main():
    ed.quit = False
    console.run()

if __name__ == '__main__':
    filename, options = ed.cmd_options()
    ed.startup(*filename, **options)
    main()

