"""
edsel_command.py - Edsel display editor with Command class, but no
 Job.  Use command and key modules instead of Python input to get
 command line one character at a time.  BUT use blocking event loop,
 not Piety scheduler.
"""

import edsel, command, key, keyboard

# Here we use Command args rather than calling edsel functions in main()
edselc = command.Command(handler=key.Key(), do_command=edsel.cmd,
                         stopped=(lambda command: 
                                  edsel.ed.quit or command == keyboard.C_d))

def main():
    edsel.ed.quit = False # previous quit might have set it True
    edsel.init_session(c=12) # 12 lines in scrolling command region
    edselc.restart()
    while not edselc.stopped():
        edselc.handler()   # q command sets edsel.ed.quit True, forces exit
    edselc.restore() # restores terminal, different from restore_display
    edsel.restore_display()

if __name__ == '__main__':
    main()
