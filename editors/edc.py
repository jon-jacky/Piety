"""
edc.py - Run *ed.py* line editor.  Use *console* module
  instead of Python builtin *input()* to collect and edit
  input lines.  Contrast to *ed.py* *main* function and *etty.py*.
"""

import ed, console as con

def ed_command_mode():
    'Used by ed_specialmodes arg to select prompt'
    if ed.command_mode and not ed.pysh.continuation:
        return 'ed_command'
    elif ed.command_mode and ed.pysh.continuation:
        return 'pysh_continuation'
    else: # not ed.command_mode:
        return 'ed_input'

ed_specialmodes = { 'ed_input': ('', con.command_keymap),
                    'pysh_continuation': (ed.pysh.ps2, con.command_keymap)}

console = con.Console(prompt=':', do_command=ed.do_command,
                      stopped=(lambda command: ed.quit),
                      mode=ed_command_mode,
                      specialmodes=ed_specialmodes)

def main():
    ed.startup()
    console.run()

if __name__ == '__main__':
    main()
