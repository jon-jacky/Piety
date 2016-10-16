"""
eden.py - run *edsel.py* display editor, with additional screen
 editing commands. Use *command*, *lineinput*, and *key* modules
 instead of Python builtin *input()* to collect and edit input lines.
 Contrast to *edsel.py* *main* function and *edc.py*.
"""

import edsel, command, key, lineinput, display

def cmd(chars):
    'Handle new eden commands here, pass other commands to edsel'
    if chars == 'c': # c(hange) just one line at dot, no line address range
        buf = edsel.ed.buf
        dot = buf.dot
        edenc.command_line.chars = buf.lines[dot].rstrip() # strip \n
        edenc.command_line.point = 0
        edenc.clear_chars = False # don't clear the line we just assigned
        edsel.ed.cmd_name = 'c' # needed by edsel functions, following
        edsel.ed.command_mode = False 
        buf.d(dot, dot) # ed c(hange) command deletes changed lines first
        buf.dot = dot - 1 # buf.d updates buf.dot to the line after delete
        edsel.maintain_display()
        edsel.update_display()
    else:
        edsel.cmd(chars)

edenc = command.Command(prompt=':', reader = key.Key(),
                        command_line=lineinput.LineInput(),
                        do_command=cmd,
                        stopped=(lambda command: edsel.ed.quit),
                        keymap=command.vt_keymap,
                        mode=(lambda: edsel.ed.command_mode), # True or False
                        behavior={ False: ('', command.vt_insert_keymap) })

def main():
    edsel.ed.quit = False # previous quit might have set it True
    edsel.init_session(c=12) # 12 lines in scrolling command region
    edenc.restart()
    while (not edenc.stopped() and 
           edenc.command_line.chars not in edenc.job_control):
        edenc.handler()   # q command sets edsel.ed.quit True, forces exit
    edenc.restore() # restores terminal, different from restore_display
    edsel.restore_display()

if __name__ == '__main__':
    main()
