"""
aclock.py - Onscreen clock 
            Based on atimers.py ATimer class.
"""

import sys, asyncio
from datetime import datetime
import display, pmacs, pyshell, writer

def restore_cursor():
    'Based on writer.py restore_cursor but simpler'
    if pyshell.cmd_mode:
        writer.restore_cursor_to_cmdline()
    else: 
        pmacs.restore_cursor_to_window()
                    
class AClock():
    """
    AClock, a class so we can update instance vars while running, esp. exit
    """
    def __init__(self):
        self.row = 1 # location on display, default top row
        self.col = 136 # loc, default right edge of 146 column display
        self.n = -1 # run forever
        self.delay = 1.0 # seconds, can be edited while timer is running
        self.exit = False  # set True to exit before n runs out.

    async def aclock(self, n=-1, delay=1.0, row=1, col=136): # 146 cols, am pm
        self.row = row # location on display
        self.col = col # ditto
        self.n = n # number of ticks, -1 to run forever or until self.exit=True
        self.delay = delay
        while True: # calculate break from self.n each time
            if self.n == 0 or self.exit: break
            await asyncio.sleep(self.delay)
            # %H 24 hour clock, %I 12 hour clock %l 12 h single digits w/blank
            # %p AM PM  %P am pm
            hrminsec = datetime.now().strftime('%l:%M:%S %P')
            display.put_cursor(self.row, self.col)
            display.render(hrminsec, display.bold)  
            restore_cursor() # return cursor to prev loc in window or REPL
            if self.n > 0: self.n -= 1  # We get one tick if self.n = 1

# Global so we can read/set from REPL
# Each call to createclock reassigns these, so we can only have one clock.
loop = None; ca = None; ta = None

def createclock(n, delay, col):
    'Creates clock task but does not run the event loop, maybe already running'
    global loop, ca, ta, x
    loop = asyncio.get_event_loop() # the already running loop, if there is one
    ca = AClock()
    ta = loop.create_task(ca.aclock(n, delay, 1, col)) # row 1
        
def runclock(n, delay, col):
    'Start the clock, creates and runs the event loop for a standalone test' 
    createclock(n, delay, col) # assign global ca, ta, loop
    loop.run_until_complete(ta) # use global ta, loop
    
def stopclock():        
    global ca
    ca.exit = True
