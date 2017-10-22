"""
edselc.py - Run *edsel.py* display editor, Use *console*
  module instead of Python builtin *input* to collect and edit
  input lines.  Contrast to *edsel.py* *main* function and *eden.py*.
"""

import edc, edsel, console as con

console = con.Console(prompt=':', do_command=edsel.do_command,
                      stopped=(lambda command: edsel.ed.quit),
                      mode=edc.ed_command_mode,
                      specialmodes=edc.ed_specialmodes)

def main(*filename, **options):
    edsel.startup(*filename, **options)
    console.run()
    edsel.cleanup()

if __name__ == '__main__':
    filename, options = edsel.ed.cmd_options()
    main(*filename, **options)

