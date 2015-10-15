"""
edselc.py - Run an edsel display editor session.
 Use command and key modules instead of Python raw_input to get command line.
 BUT do not use Piety scheduler.
"""

import edsel, command, key

# Here we use Command args rather than calling edsel functions in main()
edselc = command.Command(prompt='', reader=key.Key(), handler=edsel.cmd)

def main():
    edsel.ed.quit = False # previous quit might have set it True
    edsel.init_session()
    while not edsel.ed.quit:
        if edselc.new_command:
            edselc.restart()
        edselc.reader()   # q command sets edsel.ed.quit True, forces exit
    edsel.restore_display()

if __name__ == '__main__':
    main()
