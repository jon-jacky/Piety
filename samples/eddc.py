#!/usr/bin/env python
"""
eddc.py - Run an edd display editor session.
 Use command and key modules instead of Python raw_input to get command line.
 BUT do not use Piety scheduler.
"""

import edd, command, key

eddc = command.Command(prompt='', handler=edd.cmd, stop='q')

k = key.Key(eddc.handle_key)

def main():
    edd.ed.quit = False # allow restart
    edd.init_display()
    eddc.restart()
    while not edd.ed.quit:
        k.getchar()
    edd.restore_display()

if __name__ == '__main__':
    main()
