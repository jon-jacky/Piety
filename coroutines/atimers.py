""" 
atimers.py - Coroutine that prints timestamps at intervals,
             to run in tasking experiments.

This module is named atimers (with an s) but the coroutine is named atimer 
(no s) so we can 'from atimers import atimer' without name conflict. 
"""

import sys, asyncio, datetime

# Based on timer from timers.py
async def atimer(n=1, delay=1.0, label='', destination=sys.stdout):
    """ 
    Sleep for given delay (default 1.0 sec), then print timestamp message.
    Repeat n times (default 1).  Message includes time and optional label. 
    Optional label for distinguishing output from different function calls.
    Calls print() to print output to stdout, which can be redirected.
    Calls print('...\n\r', end='') so it works in terminal char and line modes, 
    """
    for i in range(n):
        await asyncio.sleep(delay)
        # For now use print with default args, which adds the \n itself.
        print(f'{label} {i+1} {datetime.datetime.now()}\n\r', end='',
              file=destination)

class ATimer():
    """
    ATimer class, here delay and run are instance vars
    so we can control multiple timers independently
    """
    def __init__(self):
        self.delay = 1.0 # can be edited while timer is running
        self.run = True  # set False to exit before n runs out.

    async def atimer(self, n=1, delay=1.0, label='', destination=sys.stdout):
        """
        destination must be a file-like object, must have a write method.
        """
        self.delay = delay
        self.run = True
        for i in range(n):
            if not self.run: break
            await asyncio.sleep(self.delay)
            if destination == sys.stdout: # default
                print(f'{label} {i+1} {datetime.datetime.now()}\n\r', end='',
                      file=destination)
            # We found that redirection with print(..., file=...)
            #  does not work well with our Writer objects when threading.
            # Instead, just calling the object's write method does work.
            else:
                destination.write(f'{label} {i+1} {datetime.datetime.now()}\n\r')


