"""
edc.py - Run *ed.py* line editor.  Use *console* module
  instead of Python builtin *input()* to collect and edit
  input lines.  Contrast to *ed.py* *main* function and *etty.py*.
"""

import ed, console as con

console = con.Console(prompt=':', do_command=ed.do_command,
                      stopped=(lambda command: ed.quit),
                      mode=(lambda: ed.command_mode))

def main():
    ed.startup()
    console.run()

if __name__ == '__main__':
    main()
