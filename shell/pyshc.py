"""
pyshc.py - Run a pysh Python shell session.
 Use console module instead of Python input to enter and edit command line.
 Contrast to pysh.py main function.
"""

import pysh, console as con

console = con.Console(prompt='>> ', do_command=pysh.do_command,
                      stopped=(lambda command: not pysh.running),
                      mode=(lambda: not pysh.more), 
                      specialmodes={False: ('.. ', con.command_keymap)})

def main():
    'Python REPL using home-made pysh shell'
    print("pysh shell, type any Python statement, exit() or ^D to exit")
    console.run()

if __name__ == '__main__':
    main()
