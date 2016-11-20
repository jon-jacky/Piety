"""
eden.py - run *edsel.py* display editor, with additional screen
 editing commands. Use *command*, *lineinput*, and *key* modules
 instead of Python builtin *input()* to collect and edit input lines.
 Contrast to *edsel.py* *main* function and *edselc.py*.
"""

import edsel, console as con, key, lineinput

c_command, buf, dot = False, None, 0

# Ths cmd called from accept_command or accept_line, via do_command
def do_command(chars):
    'Handle new eden commands here, pass other commands to edsel'
    global c_command, buf, dot

    # command mode, 'c' with no address range, c(hange) just one line
    if edsel.ed.command_mode and chars == 'c':
        c_command = True
        buf = edsel.ed.buf
        dot = buf.dot
        console.initline = buf.lines[dot].rstrip() # strip \n at eol
        console.initpoint = 0
        edsel.ed.cmd_name = 'c' # needed by edsel functions, following
        edsel.ed.command_mode = False 
        edsel.win.put_update_cursor()

    # inline c command finished, assign updated line and update
    elif not edsel.ed.command_mode and c_command:
        buf.lines[dot] = console.command.line + '\n'
        edsel.ed.command_mode = True
        c_command = False    
        edsel.update_display() # maintain not needed, no insert/delete/move

    # pass all other commands to edsel
    else:
        edsel.do_command(chars)

console = con.Console(prompt=':', reader = key.Key(),
                      command=lineinput.LineInput(),
                      do_command=do_command,
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
