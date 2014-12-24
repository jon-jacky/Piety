"""
edc.py - ed configuration that uses console and key modules
          instead of using built-in Python raw_input to get command line.
"""

import ed, console, key, line
import terminal

# Here the optional initialize and cleanup args are default None
c = console.Console(prompt='', command=ed.cmd, 
                    optional_keymap=line.keymap,
                    quit=ed.q) 

k = key.Key(c.handle_key)

def main():
    # terminal setup and restore are done for each command 
    #  by c.do_command via k.getchar
    # BUT initial c() is needed here.
    ed.quit = False
    c() # calls terminal.setup()
    console.Console.continues = True # c() set it False, must be True
    while not ed.quit:
        key = k.getchar() # calls c.handle_key
    # quit handled by c.pause called by c.handle_key via k.getchar
    terminal.restore()

if __name__ == '__main__':
    main()
