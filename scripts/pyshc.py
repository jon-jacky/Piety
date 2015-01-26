#!/usr/bin/env python
"""
pyshc.py - Run a pysh Python shell session.
 Use command and key modules instead of Python raw_input to get command line.
 BUT do not use Piety scheduler.
"""

import pysh, command, key

pyshc = command.Command(prompt='>> ',  reader=key.Key(), handler=pysh.mk_shell(),
                        # pysh ignores exit() so we must handle special case here
                        stopcmd='exit()', suspend=pysh.exit_pysh)

def main():
    'Python REPL using home-made pysh shell'
    pysh.pexit = False # previous exit have made it True
    pyshc()
    while not pysh.pexit:
        pyshc.reader() # exit() command sets psysh.pexit = True, forces exit
            
if __name__ == '__main__':
    main()
