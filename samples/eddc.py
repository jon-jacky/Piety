"""
eddc.py - edd configuration that uses console and key modules
          instead of using built-in Python raw_input to get command line.
"""

import edd, console, key, line

c = console.Console(prompt='', command=edd.cmd, 
                    optional_keymap=line.keymap,
                    resume=edd.init_display,
                    quit=edd.ed.q, pause=edd.restore_display) 

k = key.Key(c.handle_key)

def main():
    # terminal setup and restore are done for each command 
    #  by c.do_command via k.getchar
    # BUT initial c.resume is needed here.
    edd.ed.quit = False
    c() # calls edd.init_display then terminal.setup()
    while not edd.ed.quit:
        key = k.getchar() # calls c.handle_key
    # quit, cleanup by c.do_pause called by c.handle_key via k.getchar

if __name__ == '__main__':
    main()
