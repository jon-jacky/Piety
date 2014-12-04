"""
edc.py - ed configuration that uses console and key modules
          instead of using built-in Python raw_input to get command line.
"""

import ed, console, key, line

# Here the optional initialize and cleanup args are default None
c = console.Console(prompt='', command=ed.cmd, 
                    optional_keymap=line.keymap,
                    exit=ed.q) 

k = key.Key(c.handle_key)

def main():
    # terminal setup and restore are done for each command 
    #  by c.do_command via k.getchar
    # BUT initial c.resume is needed here.
    ed.quit = False
    c.resume() # calls terminal.setup()
    while not ed.quit:
        key = k.getchar()
    # exit handled by c.pause called by c.handle_key via k.getchar

if __name__ == '__main__':
    main()
