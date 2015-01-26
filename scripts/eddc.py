#!/usr/bin/env python
"""
eddc.py - Run an edd display editor session.
 Use command and key modules instead of Python raw_input to get command line.
 BUT do not use Piety scheduler.
"""

import edd, command, key

# Here we use Command args rather than calling edd functions in main()
eddc = command.Command(prompt='', startup=edd.init_display, 
                       reader=key.Key(), handler=edd.cmd, 
                       stopcmd='q', cleanup=edd.restore_display)

def main():
    edd.ed.quit = False # previous quit might have set it True
    eddc()
    while not edd.ed.quit:
        eddc.reader()   # q command sets edd.ed.quit True, forces exit

if __name__ == '__main__':
    main()
