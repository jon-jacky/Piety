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


