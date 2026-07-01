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

This module is based on the earlier piety0.py. We are keeping the old
piety0.py module because it appears in some older scripts and
documentation.
 
The Python asyncio library uses the name event_loop, which is different
from our name eventloop.
"""

import sys, asyncio
from pprint import pprint
import pyshell, apyshell, apmacs
 
def handler():
    if pyshell.cmd_mode:
        apyshell.apysh() # async shell
    else:
        apmacs.apmrun()  # async display editor foreground job       

piety = asyncio.get_event_loop() 
piety.add_reader(sys.stdin, handler)

def startpiety():
    """
    Alternative to piety.run_forever() 
    so you don't need to type RET to get the >>>> asyncio shell prompt
    """
    apyshell.setup()
    apyshell.running = True
    piety.run_forever()

# stoppiety = exit does not work, exits from entire Python session

def tasks():
    'Abbreviation for asyncio.all_tasks(piety)'
    pprint(asyncio.all_tasks(piety)) # pprint puts each task entry on own line
    
