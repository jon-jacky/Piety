"""
eddc.py - Run an edd display editor session.
 Use command and key modules instead of Python raw_input to get command line.
 BUT do not use Piety scheduler.
"""

import edd, command, key

# Here we use Command args rather than calling edd functions in main()
eddc = command.Command(prompt='', reader=key.Key(), handler=edd.cmd)

def main():
    edd.ed.quit = False # previous quit might have set it True
    edd.init_display()
    while not edd.ed.quit:
        if eddc.new_command:
            eddc.restart()
        eddc.reader()   # q command sets edd.ed.quit True, forces exit
    edd.restore_display()

if __name__ == '__main__':
    main()
