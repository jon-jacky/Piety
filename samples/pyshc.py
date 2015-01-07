#!/usr/bin/env python
"""
pyshc.py - Run a pysh Python shell session.
 Use command and key modules instead of Python raw_input to get command line.
 BUT do not use Piety scheduler.
"""

import pysh, command, key

quit = False

# For some reason calling exit() from pysh crashes so we provide q() instead

def q():
    'Call this function to exit from the shell'
    global quit
    quit = True

pyshc = command.Command(prompt='>> ', handler=pysh.mk_shell(), stop='q()')

k = key.Key(py.handle_key)

def main():
    global quit
    quit = False # earlier invocation might have set it True
    print "pysh shell, type any Python statement, q() to exit"
    pyshc.restart()
    while not quit:
        k.getchar()

if __name__ == '__main__':
    main()
