"""
edo.py - Run *ed.py* line editor.  Use *console* module
  instead of Python builtin *input()* to collect and edit
  input lines.  Contrast to *ed.py* *main* function and *etty.py*.
"""

import ed, pysh, console as con

# not used - just for reference 

def ed_command_mode():
    'Used by ed_specialmodes arg to select prompt'
    if ed.command_mode and not pysh.continuation:
        return 'ed_command'
    elif ed.command_mode and pysh.continuation:
        return 'pysh_continuation'
    else: # not ed.command_mode:
        return 'ed_input'

ed_specialmodes = { 'ed_input': ('', con.insert_keymap),
                    'pysh_continuation': (pysh.ps2, con.command_keymap)}

# delete above here

command_prompt = ':'
input_prompt   = ''

def do_command(line):
    'Console argument: do ed command, also manage prompts and keymaps'
    ed.do_command(line)
    console.prompt = (command_prompt if ed.command_mode else input_prompt)
    console.keymap = (con.command_keymap if ed.command_mode 
                      else con.insert_keymap)

console = con.Console(prompt=':', do_command=do_command,
                      stopped=(lambda command: ed.quit))

def main():
    ed.startup()
    console.run()

if __name__ == '__main__':
    main()
