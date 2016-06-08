"""
edselc.py - Run an edsel display editor session.
 Use command and key modules instead of Python input to get command line
 one character at a time.  BUT do not use Piety scheduler.
"""

import edsel, command, key, keyboard

# Here we use Command args rather than calling edsel functions in main()
edselc = command.Command(handler=key.Key(), do_command=edsel.cmd,
                         stopped=(lambda command: 
                                  edsel.ed.quit or command == keyboard.C_d),
                         cleanup=edsel.restore_display())

def main():
    edsel.ed.quit = False # previous quit might have set it True
    edsel.init_session()
    edselc.restart()
    while not edselc.stopped():
        edselc.handler()   # q command sets edsel.ed.quit True, forces exit


if __name__ == '__main__':
    main()
