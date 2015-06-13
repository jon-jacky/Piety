"""
pyshc.py - Run a pysh Python shell session.
 Use command and key modules instead of Python raw_input to get command line.
 BUT do not use Piety scheduler.
"""

import pysh, command, key

pyshc = command.Command(prompt='>> ',  reader=key.Key(), handler=pysh.mk_shell())

def main():
    print("pysh shell, type any Python statement, exit() to exit")
    pysh.pexit = False # previous exit have made it True
    while not pysh.pexit:
        if pyshc.new_command:
            pyshc.restart()
        pyshc.reader() # exit() command sets psysh.pexit = True, forces exit
            
if __name__ == '__main__':
    main()
