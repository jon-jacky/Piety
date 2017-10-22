"""
pyshc.py - Run a pysh Python shell session.
 Use console module instead of Python input to enter and edit command line.
 Contrast to pysh.py main function.
"""

import pysh, console as con

console = con.Console(prompt=pysh.ps1, do_command=pysh.push,
                      stopped=(lambda command: not pysh.running),
                      mode=(lambda: not pysh.continuation), 
                      specialmodes={False: (pysh.ps2, con.command_keymap)})

def main():
    'Python REPL using pysh shell'
    print("pysh shell, type any Python statement, exit() or ^D to exit")
    console.run()

if __name__ == '__main__':
    main()
