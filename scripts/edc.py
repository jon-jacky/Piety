"""
edc.py - Run an ed line editor session.
 Use command and key modules instead of Python input to get command line
 one character at a time.  BUT do not use Piety scheduler.
"""

import ed, command, key, keyboard

edc = command.Command(handler=key.Key(),  do_command=ed.cmd,
                      stopped=(lambda command: 
                               ed.quit or command == keyboard.C_d))

def main():
    ed.quit = False # previous quit might have set it True
    while not edc.stopped():
        edc.handler() # q command sets ed.quit True, forces exit

if __name__ == '__main__':
    main()
