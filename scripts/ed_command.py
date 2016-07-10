"""
edc.py - Run an ed line editor session.
 Use command and key modules instead of Python input to get command line
 one character at a time.  BUT do not use Piety scheduler.
"""

import ed, command, key, keyboard

edc = command.Command(prompt=': ', reader=key.Key(),  do_command=ed.cmd,
                      stopped=(lambda command: ed.quit))

def main():
    ed.quit = False # previous quit might have set it True
    edc.restart()
    while not edc.stopped() and edc.command not in edc.job_control:
        edc.handler() # q command sets ed.quit True, forces exit
    edc.restore()

if __name__ == '__main__':
    main()
