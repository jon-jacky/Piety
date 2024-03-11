"""
timers.py - functions to run in tasking experiments.

This module is named timers (plural).  It contains a function named 
timer (single).  So we can say 'from timers import timer' and later
'reload timers' with no name clash.

threads.txt explains how to do some experiments with these functions.
"""

import time, datetime, sys
import edsel # used by etimer and ptimer

# This timer writes to stdout, can be redirected

def timer(n=1, delay=1.0, label=''):
    """ 
    Sleep for given delay (default 1.0 sec), then print timestamp message.
    Repeat n times (default 1).  Message includes time and optional label. 
    Optional label for distinguishing output from different function calls.
    Calls print() to print output to stdout, which can be redirected.
    Calls print('...\n\r', end='') so it works in terminal char and line modes, 
    """
    for i in range(n):
        time.sleep(delay)
        # For now use print with default args, which adds the \n itself.
        print(f'{label} {i+1} {datetime.datetime.now()}\n\r', end='')
  
# This timer uses print(..., destination=...) to write to any buffer.

def ptimer(n=1, delay=1.0, label='', destination=sys.stdout):
    """
    Similar to timer function above, but instead of print() to stdout,
    has an additional destination argument which can be any object with 
    a method named write.  destination can be a Writer object that 
    writes to any editor buffer.  Default destination writes to REPL.
    """
    for i in range(n):
        time.sleep(delay)
        print(f'{label} {i+1} {datetime.datetime.now()}\n\r', end='',
        file=destination)

vdelay = 1.0 # used by vtimer below, can be edited while vtimer is running
vrun = True  # used by vtimer, set False to exit before n runs out.

def vtimer(n=1, delay=1.0, label='', destination=sys.stdout):
    'Like ptimer above, but uses global vdelay that can be edited while running'
    global vdelay, vrun
    vdelay = delay
    vrun = True # in case it was set False on an earlier run
    for i in range(n):
        if not vrun: break
        time.sleep(vdelay)
        print(f'{label} {i+1} {datetime.datetime.now()}\n\r', end='',
        file=destination)

class Timer():
    """
    Timer class, like vtimer fcn above but here delay and run are instance varss
    so we can control multiple timers independtly
    """
    def __init__(self):
        self.delay = 1.0 # can be edited while vtimer is running
        self.run = True  # set False to exit before n runs out.

    def timer(self, n=1, delay=1.0, label='', destination=sys.stdout):
        self.delay = delay
        self.run = True # in case it was set False on an earlier run
        for i in range(n):
            if not self.run: break
            time.sleep(self.delay)
            print(f'{label} {i+1} {datetime.datetime.now()}\n\r', end='',
            file=destination)




