"""
eventloop.py - Creates BUT DOES NOT START an asyncio event loop named
 piety that responds to terminal keystrokes. Our shells and editors run
 in this event loop, and it can also run other asyncio tasks.

 Also defines the startpiety and tasks functions.
 
Type startpiety() at the >>> prompt. Then the ansyncio prompt >>>> will
appear immediately.

To stop the event loop and pause all the tasks it is running, type ^D or
at the >>>> prompt. Now you see the >>> prompt again to indicate
you are running in the standard Python REPL.  You can restart the event
loop and resume the tasks by typing piety_start() again.

This module is based on an earlier module named piety.py, now renamed to
piety0.py so we can name our startup script piety.py. We are keeping the
old piety0.py module because it appears in some older scripts and
documentation.
 
The Python asyncio library uses the name event_loop, which is different
from our name eventloop.
"""

import sys, asyncio
from pprint import pprint
import pyshell, apyshell, apmacs
import aclock, terminal_util  # just for clock called from startpiety
 
def handler():
    if pyshell.cmd_mode:
        apyshell.apysh() # async shell
    else:
        apmacs.apmrun()  # async display editor foreground job       

piety = asyncio.get_event_loop() # piety is the name of our event loop object
piety.add_reader(sys.stdin, handler) # enable shell and editor to run in loop

col = 1 # Assigned from startpiety body

def startpiety():
    """
    Alternative to piety.run_forever() 
    so you don't need to type RET to get the >>>> asyncio shell prompt
    """
    global col # DEBUG - investigate why startclock called here doesn't work
    apyshell.setup()
    apyshell.running = True
    piety.run_forever()
    # For some reason, startclock has no effect when called here
    # tlines, tcols = terminal_util.dimensions()
    # col = tcols - 10 # 10 not 11 for hh:mm:ss am  #DEBUG assign global col
    # aclock.startclock0(-1, 1, col) # runclock() gets RunTimeError: loop exists
    
# stoppiety = exit  does not work, exits from entire Python session
#                   for now use ^D to exit from >>>> back to >>>
    
def tasks():
    'Abbreviation for asyncio.all_tasks(piety)'
    pprint(asyncio.all_tasks(piety)) # pprint puts each task entry on own line
    
