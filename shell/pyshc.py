"""
pyshc.py - Run a pysh Python shell session.
 Use command and key modules instead of Python raw_input to get command line.
 BUT do not use Piety scheduler.
"""

import pysh, command, key

pyshc = command.Command(prompt='>> ',  reader=key.Key(), handler=pysh.mk_shell())

def main():
    'Python REPL using home-made pysh shell'
    pysh.start()
    print("pysh shell, type any Python statement, exit() to exit")
    while pysh.running:
        if pyshc.new_command:
            pyshc.restart()
        pyshc.reader() # exit() command sets pysh.running = False, forces exit
            
if __name__ == '__main__':
    main()
