"""
etty.py - Run ed line editor session, but use console/command.py
 instead of Python input() to collect and edit command line and inserted text.
Use keymaps to provide retro printing-terminal-style editing and history.
"""

import ed, command, key, keyboard

edc = command.Command(prompt=':', do_command=ed.cmd,
                      stopped=(lambda command: ed.quit),
                      keymap=command.printing_command_keymap,
                      mode=(lambda: ed.command_mode), # True or False
                      behavior={ False: ('', command.printing_insert_keymap) })

def main():
    ed.quit = False # previous quit might have set it True
    edc.restart()
    while (not edc.stopped() and 
           edc.command_line.chars not in edc.job_control):
        edc.handler() # q command sets ed.quit True, forces exit
    edc.restore()

if __name__ == '__main__':
    main()
