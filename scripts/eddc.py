#!/usr/bin/env python
"""
eddc.py - Run an edd display editor session.
 Use command and key modules instead of Python raw_input to get command line.
 BUT do not use Piety scheduler.
"""

import edd, command, key

eddc = command.Command(run=edd.init_display, prompt='', handler=edd.cmd, 
                       stop=edd.restore_display, stopcmd='q')

k = key.Key(eddc.handle_key)

def main():
    edd.ed.quit = False # allow restart
    eddc()
    while not edd.ed.quit:
        k.getchar()

if __name__ == '__main__':
    main()
