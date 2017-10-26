"""
wyshka.py - Run a pysh Python shell session.
 Use console module instead of Python input to enter and edit command line.
 Contrast to pysh.py main function.
"""

import pysh, console as con

def do_command(line):
    'Console argument: do pysh command, also manage continuation line prompt'
    pysh.push(line)
    console.prompt = pysh.ps2 if pysh.continuation else pysh.ps1

console = con.Console(prompt=pysh.ps1, do_command=do_command,
                      stopped=(lambda command: not pysh.running))

def main():
    'Python REPL using pysh shell'
    print("pysh shell, type any Python statement, exit() or ^D to exit")
    console.run()

if __name__ == '__main__':
    main()
