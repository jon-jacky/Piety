"""
pysh_console.py - Run a pysh Python shell session.
 Use console and key modules instead of Python raw_input to get command line.
 BUT do not use Piety scheduler.
"""

import pysh, console as con, key, lineinput

console = con.Console(prompt='>> ', reader=key.Key(), 
                      command=lineinput.LineInput(),
                      do_command=pysh.mk_shell(),
                      keymap=con.vt_keymap,
                      stopped=(lambda command: not pysh.running))

def main():
    'Python REPL using home-made pysh shell'
    print("pysh shell, type any Python statement, exit() or ^D to exit")
    console.run()

if __name__ == '__main__':
    main()
