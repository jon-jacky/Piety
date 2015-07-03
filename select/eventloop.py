"""
eventloop - An event loop with a run method.

This is a platform-dependent module. It uses the select module, so it
must run on a Unix-like host OS (including Linux and Mac OS X).  One
of the select channels is stdin (which I recall does *not* work
in the Windows version of select).

This is imported by the piety module, then the piety module shares data, see below
"""

import datetime, select
from schedule import handler, ievent, timer, start, stop
import schedule # for schedule, period, running

def adjust_interval(t0, interval):
    'Adjust timeout to occur after with the same interval despite delay'
    t1 = datetime.datetime.now()
    dt = t1 - t0
    dt_sec = dt.seconds + 0.000001*dt.microseconds
    interval = interval - dt_sec # should never be negative ...
    return interval if interval > 0.0 else schedule.period # ... but ...

# Used by select in event loop
inputs, outputs, exceptions = [],[],[]

# The eventloop API: activate, deactivate, start, stop

def activate(t):
    """
    Activate task t by adding t.input to eventloop inputs list
    This should only be called after task t has been added to schedule.
    """
    if t.input != timer and t.input not in inputs:
        inputs.append(t.input)
        
def deactivate(t):
    """
    De-activate task t by deleting t.input from eventloop inputs list
    This should only be called after t has been removed from schedule
    """
    # Only remove t.input when no more tasks in schedule use that input
    if t.input not in schedule.schedule:
        if t.input in inputs:
            inputs.remove(t.input)
    
def run(nevents=0):
    """
    Run the Piety event loop.
    nevents: number of timer events to process, then exit run loop.
     If nevents not 0, runs even if running==False
     Use default nevents=0 to process until running==False or unhandled exception
    """
    start()
    maxevents = ievent[timer] + nevents # ievent includes previous calls to run()
    interval = schedule.period # timeout interval in seconds, uses global period
    while schedule.running or (nevents and ievent[timer] < maxevents):
        # Python select doesn't assign time remaining to timeout argument
        # so we have to time it ourselves
        t0 = datetime.datetime.now()
        inputready, outputready, exceptready = select.select(inputs, outputs,
                                                             exceptions, interval)
        # inputs
        for fd in inputready:
            handler(fd)
            interval = adjust_interval(t0, interval)

        # periodic timeout if no input
        if not (inputready or outputready or exceptready): 
            handler(timer)
            interval = schedule.period # if we got here, full interval has elapsed
