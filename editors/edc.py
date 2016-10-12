"""
edselc.py - run *ed.py* line editor, use *command*, *lineinput*, and
  *key* modules instead of Python builtin *input()* to collect and edit
  input lines.  Contrast to *ed.py* *main* function and *etty.py*.
"""

import ed, command, lineinput, key

edc = command.Command(prompt=':', reader = key.Key(),
                      command_line=lineinput.LineInput(),
                      do_command=ed.cmd,
                      stopped=(lambda command: ed.quit),
                      keymap=command.vt_keymap,
                      mode=(lambda: ed.command_mode), # True or False
                      behavior={ False: ('', command.vt_insert_keymap) })

def main():
    ed.quit = False # previous quit might have set it True
    edc.restart()
    while (not edc.stopped() 
           and edc.command_line.chars not in edc.job_control):
        edc.handler() # q command sets ed.quit True, forces exit
    edc.restore()

if __name__ == '__main__':
    main()
