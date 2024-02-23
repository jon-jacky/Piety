"""
threads.py - Tasking experiments with threads
"""

import time, datetime
from threading import Thread
from contextlib import redirect_stdout
import edsel # used by etimer and ptimer


# This timer prints to stdout.
# Output can be redirected to any object with a write method 
# by using "with redirect_stdout ..."

def timer(n=1, delay=1.0, label=''):
    """ 
    Sleep for given delay (default 1.0 sec), then print messsage.
    Repeat n times (default 1).  Message includes timestamp and optional label. 
    Optional label for distinguishing output from different function calls.
    Calls print() to print output to stdout, which can be redirected.
    """
    for i in range(n):
        time.sleep(delay)
        # For now use print with default args, which adds the \n itself.
        print(f'{label} {i+1} {datetime.datetime.now()}')

# Threads that call timer 3 times, after 5 sec delay, with given label A or B
ta = Thread(target=timer,args=(3,5,'A'))
tb = Thread(target=timer,args=(3,5,'B'))

# To interleave printing messages in the scrolling REPL
# type these commands at the REPL prompt.
# Be sure to use the Thread start() method to run them in the background.
#   
# >>> ta.start()
# >>> tb.start()
#
# The edsel module contains a write function that appends a string
# to the editor buffer and displays the buffer in the focus window.
# To print messages from one thread in the focus window,
# type these commands at the REPL prompt. 
# Be sure to use the Thread run method, not the start method.
# This thread runs in the foreground so it can't interleave with another.
#
# >>> from contextlib import redirect_stdout
# >>> with redirect_stdout(edsel) as f: ta.run()
## If you call ta.start() instead the messages print in the REPL.  
    
# This timer calls edsel.write() to write to editor buffer and display

def etimer(n=1, delay=1.0, label=''):
    """
    Like timer function (above), same args, but instead of print() to stdout,
    this timer calls edsel.write() to write to current buffer and focus window
    """
    for i in range(n):
        time.sleep(delay)
        edsel.write(f'{label} {i+1} {datetime.datetime.now()}')

eta = Thread(target=etimer,args=(3,5,'A'))
etb = Thread(target=etimer,args=(3,5,'B'))

# To interleave printing messages in focus window
# type these commands at the REPL prompt:
#   
# >>> eta.start()
# >>> etb.start()
 
# This timer uses print(..., destination=...) to write to any edsel buffer.

def ptimer(n=1, delay=1.0, label='', destination=edsel):
    """
    Similar to timer function above, but instead of print() to stdout,
    has an additional destination argument which can be any object with 
    a method named write.  destination can be a Writer object that 
    writes to any edsel buffer.  Default destination writes to current buffer.
    """
    for i in range(n):
        time.sleep(delay)
        # For now use print with default args, which adds the \n itself.
        # Try to print using edsel module's write function.
        print(f'{label} {i+1} {datetime.datetime.now()}', file=destination)

pta = Thread(target=ptimer,args=(3,5,'A'))
ptb = Thread(target=ptimer,args=(3,5,'B'))

# To interleave printing messages in focus window
# type these commands at the REPL prompt:
#
# >>> ptb.start()
# >>> pta.start()
#
# Create Writer objects (see edsel for explanation):
# These only work if the session includes text buffers named a.txt and b.txt

abuf = edsel.Writer('a.txt')
bbuf = edsel.Writer('b.txt')

# (Recall that a and b are the names of the sked/edsel append and buffer 
# functions (commans), so we can't use a = Writer('a.txt') etc.)
#
# We find that these do not interleave:
#
# >>> with redirect_stdout(abuf) as buf: pta.start()
# >>> with redirect_stdout(bbuf) as buf: ptb.start()
#
# The preceding code nests the thread inside the redirect.  
# We also tried nesting the redirect inside the thread:

def fta():
    with redirect_stdout(abuf) as buf: timer(10,5,'A')

def ftb():
    with redirect_stdout(bbuf) as buf: timer(10,5,'B')

# Then these interleave, but output is not always printed 
# to intended destinations:
#
# >>> Thread(target=fta).start() 
# >>> Thread(target=ftb).start() 
# 
# Indeed, official docs say this doesn't work:
#
# From https://docs.python.org/3/library/contextlib.html
#
# "contextlib.redirect_stdout(new_target)
# Context manager for temporarily redirecting sys.stdout to another file
# or file-like object. ...
#
# Note that the global side effect on sys.stdout means that this context
# manager is not suitable for use in library code and most threaded
# applications. It also has no effect on the output of subprocesses.
# However, it is still a useful approach for many utility scripts."
  
