"""
edselc.py - Run *edsel.py* display editor, Use *console*
  module instead of Python builtin *input* to collect and edit
  input lines.  Contrast to *edsel.py* *main* function and *eden.py*.
"""

import edsel, console as con

console = con.Console(prompt=':', do_command=edsel.do_command,
                      stopped=(lambda command: edsel.ed.quit),
                      mode=(lambda: edsel.ed.command_mode))

def main():
    edsel.ed.quit = False # previous quit might have set it True
    edsel.startup(c=12) # 12 lines in scrolling command region
    console.run()
    edsel.cleanup()

if __name__ == '__main__':
    main()
