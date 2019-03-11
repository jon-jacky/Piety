"""
salysh.py - Defines the pysh Console job that wraps the pysh.py Python shell.
             Contrast to pysh.py main function.
"""

import pysh as repl, console

pysh = console.Console(prompt=(lambda: repl.prompt), process_line=repl.push,
                       stopped=(lambda command: not repl.running),
                       startup=repl.start, cleanup=repl.stop)

def main():
    'Python REPL using pysh shell'
    print("pysh shell, type any Python statement, exit(), ^D, or ^Z to exit")
    pysh.run()

if __name__ == '__main__':
    main()
