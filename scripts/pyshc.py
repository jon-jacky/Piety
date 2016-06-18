"""
pyshc.py - Run a pysh Python shell session.
 Use command and key modules instead of Python raw_input to get command line.
 BUT do not use Piety scheduler.
"""

import pysh, command, key

pyshc = command.Command(prompt='>> ',  handler=key.Key(), do_command=pysh.mk_shell(),
                        stopped=(lambda command: not pysh.running))

def main():
    'Python REPL using home-made pysh shell'
    print("pysh shell, type any Python statement, exit() to exit")
    pysh.start()
    pyshc.restart()
    while not pyshc.stopped():
        pyshc.handler()
            
if __name__ == '__main__':
    main()
