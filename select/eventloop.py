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

# Used by select in event loop
inputs, outputs, exceptions = [],[],[]

timer = -1 # indicates timer input, not timeout interval. Differs from any fd.fileno()

# Count events on each input. key: input, value: number of events on that input
# This item is global so it can be for enabling conditions and handlers.
ievent = Counter()

def activate(t):
    """
    Activate task t by adding t.input to eventloop inputs list and ievent counter
    This should only be called after task t has been added to schedule.
    """
    if t.input != timer and t.input not in inputs:
        inputs.append(t.input)
    if t.input not in ievent:
        ievent[t.input] = 0
        
def deactivate(t):
    """
    De-activate task t by deleting t.input from eventloop inputs list and ievent cntr.
    This should only be called after t has been removed from schedule
    """
    # Only remove t.input when no more tasks in schedule use that input
    if t.input not in schedule:
        if t.input in inputs:
            inputs.remove(t.input)
        if t.input in ievent:
            del ievent[t.input]

done = False  # can exit on demand

def quit():
    'Exit from Piety event loop'
    global done
    done = True # must reset to False before we can resume
    
def run(nevents=0):
    """
    Run the Piety event loop.
    period: event loop period, default 1 sec
    nevents: number of timer events to process, then exit run loop.
              use default nevents=0 
              to process until done=True or unhandled exception
    """
    global ievent # must be global for enabling conditions and handlers
    maxevents = ievent[timer] + nevents # when to stop
    interval = period # timeout INTERVAL in seconds, uses global period
    # counts timeout events, for all events ... or sum(ievent.values()) < ..
    while not done and (not nevents or ievent[timer] < maxevents):
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
                # if schedule is consistent with inputs, this should be unreachable.
                # if no handler, consume input anway - is this necessary?
                # s = fd.readline() # FIXME? works on stdin, fd.read() hangs
                # This module must not assume there is a console - no print allowed
                # print 'unhandled input from fd %s: %s' % (fd, s)
                pass
            ievent[fd] += 1
            interval = adjust_interval(t0, interval)

        # periodic timeout if no input
        if not (inputready or outputready or exceptready): 
            if timer in schedule:
                for t in schedule[timer]:
                    if t.enabled():
                        t.handler()
                        # no break needed - there is no data to consume
            else:
                pass # if no timer handler, just continue
            interval = period # if we got here, full interval has elapsed
            ievent[timer] += 1
