#!/usr/bin/env python
"""
edc.py - Run an ed line editor session.
 Use command and key modules instead of Python raw_input to get command line.
 BUT do not use Piety scheduler.
"""

import ed, command, key

edc = command.Command(prompt='', handler=ed.cmd, reader=key.Key())

def main():
    ed.quit = False # previous quit might have set it True
    edc()
    while not ed.quit:
        edc.reader() # q command sets ed.quit True, forces exit

if __name__ == '__main__':
    main()
