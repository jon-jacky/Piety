"""
edselc.py - run *edsel.py* display editor, use *command*, *lineinput*, and
  *key* modules instead of Python builtin *input()* to collect and edit
  input lines.  Contrast to *edsel.py* *main* function and *eden.py*.
"""

import edsel, console as con, key, lineinput

console = con.Console(prompt=':', reader = key.Key(),
                      command=lineinput.LineInput(),
                      do_command=edsel.do_command,
                      stopped=(lambda command: edsel.ed.quit),
                      keymap=con.vt_keymap,
                      mode=(lambda: edsel.ed.command_mode), # True or False
                      behavior={ False: ('', con.vt_insertmode_keymap) })

def main():
    edsel.ed.quit = False # previous quit might have set it True
    edsel.init_session(c=12) # 12 lines in scrolling command region
    console.restart()
    while (not console.stopped() and 
           console.command.line not in console.job_commands):
        console.handler()   # q command sets edsel.ed.quit True, forces exit
    console.restore() # restores terminal, different from restore_display
    edsel.restore_display()

if __name__ == '__main__':
    main()
