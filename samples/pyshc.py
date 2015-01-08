#!/usr/bin/env python
"""
pyshc.py - Run a pysh Python shell session.
 Use command and key modules instead of Python raw_input to get command line.
 BUT do not use Piety scheduler.
"""

import pysh, command, key

pyshc = command.Command(prompt='>> ', handler=pysh.mk_shell(), stop='exit()')

k = key.Key(pyshc.handle_key)

def main():
    'Python REPL using home-made pysh shell'
    pysh.pexit = False # earlier invocation might have set it True
    print "pysh shell, type any Python statement, exit() or Ctrl-D to exit"
    pyshc.restart()
    while not pysh.pexit:
        k.getchar()

if __name__ == '__main__':
    main()
