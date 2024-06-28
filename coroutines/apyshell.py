"""
apyshell.py - Custom Python REPL in the asyncio event loop.

Structure based on aterminal.py.  Calls pyshell.py functions to do all the work.
"""

import sys, asyncio
import key
import terminal as term  
import pyshell as sh

tl = term.set_line_mode # Type tl() to restore terminal echo etc. after a crash.

loop = asyncio.get_event_loop()

def setup():
    'Assign new prompt strings, then call sh.setup.'
    # This is a hack to avoid making ps1 ps2 start_col arguments to sh.runcmd
    # FIXME?  Save prompt strings so they can be restored?
    sh.ps1 = '>>>> ' # different from CPython >>> and pyshell >>
    sh.ps2 = '.... ' # line up with async_ps1 and async_start_col
    sh.start_col = 5 # not 3
    sh.setup()

def restore():
    'Stop the event loop, but dont close it. Restore prompts, call sh.restore.'
    # FIXME?  Any reason to restore prompt strings here?
    loop.stop() # escape from run_forever()
    sh.restore()

def runcmd(c):
    'Call pyshell runcmd, test for exit, if exit call restore.'
    if (c == key.C_d and sh.cmd == '') or (sh.cmd == 'exit()'):
        restore() 
    sh.runcmd(c) # handles C_d differently when sh.cmd is not empty

def handler():
    'Run each time sys.stdin detects a new character.  Read the char, call runcmd.'
    c = term.getchar()
    runcmd(c)
 
loop.add_reader(sys.stdin, handler) # FIXME?  Use tty not stdin, as in display.py?

def main():
    'Call setup and start the event loop.  Event loop was created at module level.'
    setup()
    loop.run_forever()

if __name__ == '__main__': 
    main()
    loop.close()






