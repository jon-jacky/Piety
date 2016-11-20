"""
edc.py - run *ed.py* line editor, use *command*, *lineinput*, and
  *key* modules instead of Python builtin *input()* to collect and edit
  input lines.  Contrast to *ed.py* *main* function and *etty.py*.
"""

import ed, console as con, lineinput, key

console = con.Console(prompt=':', reader = key.Key(),
                      command=lineinput.LineInput(),
                      do_command=ed.do_command,
                      stopped=(lambda command: ed.quit),
                      keymap=con.vt_keymap,
                      mode=(lambda: ed.command_mode), # True or False
                      behavior={ False: ('', con.vt_insertmode_keymap) })

def main():
    ed.quit = False # previous quit might have set it True
    console.restart()
    while (not console.stopped() 
           and console.command.line not in console.job_commands):
        console.handler() # q command sets ed.quit True, forces exit
    console.restore()

if __name__ == '__main__':
    main()
