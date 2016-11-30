"""
pyshc.py - Run a pysh Python shell session.
 Use console module instead of Python input to enter and edit command line.
 Contrast to pysh.py main function.
"""

import pysh, console as con

console = con.Console(prompt='>> ', do_command=pysh.mk_shell(),
                      stopped=(lambda command: not pysh.running))

def main():
    'Python REPL using home-made pysh shell'
    print("pysh shell, type any Python statement, exit() or ^D to exit")
    console.run()

if __name__ == '__main__':
    main()
