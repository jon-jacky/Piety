"""
timers.py - functions etc. for tasking experiments
"""

import time, datetime
from threading import Thread
import edsel # used by etimer and ptimer


# This timer prints to stdout

def timer(n=1, delay=1.0, label=''):
    """
    Sleep for given delay (default 1.0 sec), then print messsage.
    Repeat n times (default 1).  Message includes timestamp and optional label. 
    Optional label for distinguishing output from different function calls.
    """
    for i in range(n):
        time.sleep(delay)
        # For now use print with default args, which adds the \n itself.
        print(f'{label} {i+1} {datetime.datetime.now()}') # \n\r', end='')

# Call timer 3 times, after 5 sec delay, with given label
ta = Thread(target=timer,args=(3,5,'A'))
tb = Thread(target=timer,args=(3,5,'B'))
# To interleave printing messages in the scrolling REPL
# type these commands at the REPL prompt.
# Be sure to use the Thread start() method to run them in the background.
#   
# >>> ta.start()
# >>> tb.start()
#
# To interleave printing messages in the focus window
# type these commands at the REPL prompt. 
# Be sure to use the Thread run method, not the start method.
#
# >>> from contextlib import redirect_stdout
# >>> with redirect_stdout(edsel) as f: ta.run()
# >>> with redirect_stdout(edsel) as f: tb.run()
  
#   
# This timer calls edsel.write() to write to ed current buffer and display

def etimer(n=1, delay=1.0, label=''):
    """
    Sleep for given delay (default 1.0 sec), hen write message to edsel buffer.
    Repeat n times (default 1).  Message includes timestamp and optional label. 
    Optional label for distinguishing output from different function calls.
    """
    for i in range(n):
        time.sleep(delay)
        edsel.write(f'{label} {i+1} {datetime.datetime.now()}')

eta = Thread(target=etimer,args=(3,5,'A'))
etb = Thread(target=etimer,args=(3,5,'B'))# To interleave printing messages in focus window
# type these commands at the REPL prompt:
#   
# >>> eta.start()
# >>> etb.start()


# This timer prints to ed.buffer 

def ptimer(n=1, delay=1.0, label=''):
    """
    Sleep for given delay (default 1.0 sec), then print msg on ed.buffer
    Repeat n times (default 1).  Message includes timestamp and optional label. 
    Optional label for distinguishing output from different function calls.
    """
    for i in range(n):
        time.sleep(delay)
        # For now use print with default args, which adds the \n itself.
        # Try to print using edsel module's write function.
        print(f'{label} {i+1} {datetime.datetime.now()}', file=edsel)

pta = Thread(target=ptimer,args=(3,5,'A'))
ptb = Thread(target=ptimer,args=(3,5,'B'))

# To interleave printing messages in focus window
# type these commands at the REPL prompt:
#   
# >>> pta.start()
# >>> ptb.start()


