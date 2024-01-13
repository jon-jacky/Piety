"""
timers.py - functions etc. for tasking experiments
"""

import time, datetime

def timer(n=1, delay=1.0, label=''):
    """
    Sleep for given delay (default 1.0 sec), then print messsage.
    Repeat n times (default 1).  Message includes timestamp and optional label. 
    Optional label for distinguishing output from different function calls.
    """
    for i in range(n):
        time.sleep(delay)
        print(f'{label} {i+1} {datetime.datetime.now()}\n\r', end='')

