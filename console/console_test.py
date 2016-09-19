"""
console_test.py - test console, lineinput, key modules together
"""

import command, lineinput, key

# echo completed input lines
c = command.Command(prompt='> ', reader=key.Key(), 
                    command_line=lineinput.LineInput(),
                    do_command=(lambda command: print(command)))

def main():
    c.restart()
    while c.command_line.chars not in c.job_control: # use job control for exit
        c.handler()
    c.restore()

if __name__ == '__main__':
    main()
