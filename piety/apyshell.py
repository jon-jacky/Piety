"""
apyshell.py - Adapt our pysh custom Python shell to run in an asyncio event loop.
              Define the asyncio reader function apysh that handles each shell 
              keystroke.

Structure based on aterminal.py.  Calls pyshell.py functions to do all the work.
"""

import sys, asyncio
import key
import terminal as term  
import pyshell as sh
import apmacs # apmacs.apm() starts asyncio display editor in runcmd special case

loop = None # must be global, used in both restore() and main()
running = False # loop is running, assigned by restore and apysh
 
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
    global running
    eventloop = asyncio.get_event_loop() # get the running event loop 
    eventloop.stop() # escape from run_forever()
    running = False
    sh.restore()

def runcmd(c):
    'Call pyshell runcmd, but handle two special cases. See unline comments.'
    # 1. First test for exit, if exit call restore. 
    if (c == key.C_d and sh.cmd == '') or (sh.cmd == 'exit()'):
         restore() 
    # 2. After key.cr test for apm() command that starts display editing.
    # In that case do *not* call  pyshell.runcmd key.cr case which ends with 
    #  restore_cursor_to_cmdline(); pustr(prompt).  Instead handle inline here.
    elif (c == key.cr and sh.cmd == 'apm()'):
        apmacs.apm() # starts asyncio display editing
    else:
        sh.runcmd(c) # handles C_d differently when sh.cmd is not empty
 
def apysh():
    """ 
    Run each time sys.stdin detects a new character when running in cmd_mode.
    Set up terminal on first call only, on all calls call runcmd(c).
    """
    global running
    if not running:
        setup()
        running = True
    c = term.getchar() # not blocking, asyncio only calls apysh when char is ready.
    runcmd(c)
      
def main():
    'Set up event loop, setup() the terminal, and start the event loop.'
    global loop
    loop = asyncio.get_event_loop()
    loop.add_reader(sys.stdin, handler) # FIXME? tty not stdin, like display.py?
    setup()
    loop.run_forever()

if __name__ == '__main__': 
    main()
    loop.close()
      
