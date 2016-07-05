"""
pysh_command.py - Run a pysh Python shell session.
 Use command and key modules instead of Python raw_input to get command line.
 BUT do not use Piety scheduler.
"""

import pysh, command, key, keyboard

pyshc = command.Command(prompt='>> ',  handler=key.Key(), do_command=pysh.mk_shell(),
                        stopped=(lambda command: 
                                 not pysh.running or command == keyboard.C_d))

def main():
    'Python REPL using home-made pysh shell'
    print("pysh shell, type any Python statement, exit() or ^D to exit")
    pyshc.restart()
    while not pyshc.stopped():
        pyshc.handler()
    pyshc.restore()

if __name__ == '__main__':
    main()
