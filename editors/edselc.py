"""
edselc.py - run *edsel.py* display editor, use *command*, *lineinput*, and
  *key* modules instead of Python builtin *input()* to collect and edit
  input lines.  Contrast to *edsel.py* *main* function and *eden.py*.
"""

import edsel, command, key, lineinput

edselc = command.Command(prompt=':', reader = key.Key(),
                         command_line=lineinput.LineInput(),
                         do_command=edsel.cmd,
                         stopped=(lambda command: edsel.ed.quit),
                         keymap=command.vt_keymap,
                         mode=(lambda: edsel.ed.command_mode), # True or False
                         behavior={ False: ('', command.vt_insert_keymap) })

def main():
    edsel.ed.quit = False # previous quit might have set it True
    edsel.init_session(c=12) # 12 lines in scrolling command region
    edselc.restart()
    while (not edselc.stopped() and 
           edselc.command_line.chars not in edselc.job_control):
        edselc.handler()   # q command sets edsel.ed.quit True, forces exit
    edselc.restore() # restores terminal, different from restore_display
    edsel.restore_display()

if __name__ == '__main__':
    main()
