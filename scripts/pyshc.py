#!/usr/bin/env python
"""
pyshc.py - Run a pysh Python shell session.
 Use command and key modules instead of Python raw_input to get command line.
 BUT do not use Piety scheduler.
"""

import pysh, command, key

quit = False

def pexit():
    global quit
    quit = True

def banner():
    print "pysh shell, type any Python statement, exit() or Ctrl-D to exit"

pyshc = command.Command(run=banner, prompt='>> ', handler=pysh.mk_shell(), 
                        stop=pexit, stopcmd='exit()')

k = key.Key(pyshc.handle_key)

def main():
    'Python REPL using home-made pysh shell'
    global quit
    quit = False  # enable main loop, previous exit may have set this True
    pyshc()
    while not quit:
        k.getchar()

if __name__ == '__main__':
    main()
