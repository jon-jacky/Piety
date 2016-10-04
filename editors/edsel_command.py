"""
edsel_command.py - Run an edsel display editor session.

Use command and key modules instead of Python input() to get command
line one character at a time.  BUT use blocking event loop, not Piety
scheduler. Also, do not use Command mode selection facility --- so it
prints prompt and accumulates history even in insert modes.
"""

import edsel, command, key, keyboard

# Here we use Command args rather than calling edsel functions in main()
edselc = command.Command(reader=key.Key(), do_command=edsel.cmd,
                         stopped=(lambda command: edsel.ed.quit))

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
