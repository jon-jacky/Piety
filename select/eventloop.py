"""
eventloop - An event loop with a run method.

This is a platform-dependent module. It uses the select module, so it
must run on a Unix-like host OS (including Linux and Mac OS X).  One
of the select channels is stdin (which I recall does *not* work
in the Windows version of select).
"""

import sys
import datetime
from select import select
from collections import Counter

# Variables annd functions used in event loop

period = 1.000 # seconds, periodic timer for timeout events

def adjust_interval(t0, interval):
    """
    Adjust timeout to occur after with the same interval despite delay
    """
    t1 = datetime.datetime.now()
    dt = t1 - t0
    dt_sec = dt.seconds + 0.000001*dt.microseconds
    interval = interval - dt_sec # should never be negative ...
    return interval if interval > 0.0 else period # ... but ...

# Variables used by select in Piety event loop
inputs = [sys.stdin] # could add to this list
# This doesn't work - causes run loop to exit without handling other events
#outputs = [sys.stdout] 
outputs = [] # for now this works
exceptions = []
timeout = -1 # timeout EVENT not interval.  different from any fd.fileno()

# Count each kind of event, global for enabling conditions and handlers.
# key: event, value: number of occurences
ievent = Counter([sys.stdin,timeout]) 

done = False  # can exit on demand

def quit():
    'Exit from Piety event loop'
    global done
    done = True # must reset to False before we can resume
    
def run(schedule, nevents=0):
    """
    Run the Piety event loop.
    period: event loop period, default 1 sec
    nevents: number of timeout events to process, then exit run loop.
              use default nevents=0 
              to process until done=True or unhandled exception
    """
    global ievent # must be global for enabling conditions and handlers
    maxevents = ievent[timeout] + nevents # when to stop
    interval = period # timeout INTERVAL in seconds, uses global period
    # counts timeout events, for all events ... or sum(ievent.values()) < ..
    while not done and (not nevents or ievent[timeout] < maxevents):
        # Python select doesn't assign time remaining to timeout argument
        # so we have to time it ourselves
        t0 = datetime.datetime.now()
        inputready, outputready, exceptready = select(inputs, outputs,
                                                      exceptions, interval)
        # inputs
        for fd in inputready:
            if fd in schedule:
                for t in schedule[fd]:
                    if t.enabled():
                        t.handler()
                        break # we consumed data from fd, might be no more
            else:
                s = fd.readline() # works on stdin, fd.read() hangs
                print 'unhandled input from fd %s: %s' % (fd, s)
            ievent[fd] += 1
            interval = adjust_interval(t0, interval)

        # periodic timeout if no input
        if not (inputready or outputready or exceptready): 
            if timeout in schedule:
                for t in schedule[timeout]:
                    if t.enabled():
                        t.handler()
                        # no break needed - there is no data to consume
            else:
                pass # if no timeout handler, just continue
            interval = period # if we got here, full interval has elapsed
            ievent[timeout] += 1
