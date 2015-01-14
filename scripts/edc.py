#!/usr/bin/env python
"""
edc.py - Run an ed line editor session.
 Use command and key modules instead of Python raw_input to get command line.
 BUT do not use Piety scheduler.
"""

import ed, command, key

edc = command.Command(prompt='', handler=ed.cmd, stopcmd='q')

k = key.Key(edc.handle_key)

def main():
    ed.quit = False # allow restart
    edc()
    while not ed.quit:
        k.getchar()

if __name__ == '__main__':
    main()
