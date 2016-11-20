"""
etty.py - Run ed line editor session, but use console/command.py
 instead of Python input() to collect and edit command line and inserted text.
Use keymaps to provide retro printing-terminal-style editing and history.
"""

import ed, console as con, key, keyboard

console = con.Console(prompt=':', do_command=ed.do_command,
                      stopped=(lambda command: ed.quit),
                      # accept default keymap for printing terminal
                      mode=(lambda: ed.command_mode), # True or False
                      behavior={ False: ('', con.printing_insertmode_keymap) })

def main():
    ed.quit = False # previous quit might have set it True
    console.restart()
    while (not console.stopped() and 
           console.command.line not in console.job_commands):
        console.handler() # q command sets ed.quit True, forces exit
    console.restore()

if __name__ == '__main__':
    main()
