"""
console_test.py - test console, lineinput, key modules together
"""

import console as con, lineinput, key

# echo completed input lines
console = con.Console(prompt='> ', reader=key.Key(), 
                      command=lineinput.LineInput(),
                      do_command=(lambda command: print(command)),
                      keymap=con.vt_keymap) # not printing_keymap

def main():
    console.restart()
    # use job control for exit
    while console.command.line not in console.job_commands: 
        console.handler()
    console.restore()

if __name__ == '__main__':
    main()
