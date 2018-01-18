"""
salysh.py - Run a pysh Python shell session.  Use console module
 instead of Python builtin input to collect and edit inpu lines
 without blocking.  Contrast to pysh.py main function.
"""

import pysh as repl, console

pysh = console.Console(prompt=(lambda: repl.prompt), do_command=repl.push,
                       stopped=(lambda command: not repl.running),
                       startup=repl.start, cleanup=repl.stop)

def main():
    'Python REPL using pysh shell'
    print("pysh shell, type any Python statement, exit(), ^D, or ^Z to exit")
    pysh.run()

if __name__ == '__main__':
    main()
