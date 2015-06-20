"""
eventloop.py using asyncio as an alternative to select
"""

import sys
import asyncio
import datetime

### asyncio machinery

loop = asyncio.get_event_loop()

### piety machinery

# FIXME? Can't we move a lot of this back to the platform-independent piety.py?
# Look at all the duplication between this and select/eventloop.py

# used by reader_handler, below

# FIXME? I think t0 and adjust_interval are not needed in this module
# handle_timeout does it all
# I believe that, unlike select, timeout and reading inputs don't interact

# t0 is the time when we most recently started waiting for input
t0 = datetime.datetime.now()

def adjust_interval(t0, interval):
    """
    Adjust timeout to occur after with the same interval despite delay
    """
    t1 = datetime.datetime.now()
    dt = t1 - t0
    dt_sec = dt.seconds + 0.000001*dt.microseconds
    interval = interval - dt_sec # should never be negative ...
    return interval if interval > 0.0 else period # ... but ...

# This has to be global in eventloop because piety.tasks() uses it
period = 1

done = False # used in timeout_handler and also by quit() below
             # does not need to be visible outside this module

# FIXME?  Couldn't these be args to timeout_handler instead of global?
loop_nevents = 0  # 0 means run forever, may be reassigned by run() below
maxevents    = 0  # maxevents includes events from previous calls to run()

# piety module defines these variables then shares them with eventloop:
# eventloop.schedule = schedule etc. so they can be used without qualification
# schedule
# ievent
# timer

# This might seem redundant, asyncio loop can already manage  multiple readers
# BUT we still need this to handle t.enabled
def reader_handler(fd):
    # We don't call loop.stop here, only in timeout_handler.
    # global t0 # not needed here - handle_timeout is sufficient
    #for fd in inputready: #FIXME asyncio calls this for a particular fd
    if fd in schedule:
        for t in schedule[fd]:
            if t.enabled():
                t.handler()
                break # we consumed data from fd, might be no more
    else:
        # if schedule is consistent with inputs, this should be unreachable
        # if no handler, consume input anway - is this necessary?
        # s = fd.readline() # FIXME? works on stdin, fd.read() hangs
        # This module must not assume there is a console - no print allowed
        # print 'unhandled input from fd %s: %s' % (fd, s)
        pass
    # count events and restart recurring timeout
    ievent[fd] += 1
    # Hey - I don't think we need to do any of this with asyncio
    # this is all handled by handle_timeout, doesn't interact with input
    # t0 is the time when we most recently started waiting for input
    #interval = adjust_interval(t0, interval) # use previous t0
    #t0 = datetime.datetime.now() # reset t0 right before 
    #loop.call_later(interval, timeout_handler)

def timeout_handler():
    #print 'done %s, loop_nevents %s, ievent[timer] %s, maxevents %s' % \
    #     (done,loop_nevents,ievent[timer], maxevents) # DEBUG
    if done or (loop_nevents and ievent[timer] >= maxevents):
        loop.stop()
        # We also use pysh.exit to stop, in Console lineReceived handler
    else:
        # handle scheduled timeout events
        if timer in schedule:
            for t in schedule[timer]:
                if t.enabled():
                    t.handler()
        else:
            pass # if no timeout handler, just continue
        # count events and restart recurring timeout
        ievent[timer] += 1
        interval = period # if we got here, full interval has elapsed
        loop.call_later(interval, timeout_handler)

### piety eventloop API: activate, deactivate, quit, run

def activate(t):
    """
    Activate task t by registering t.input with loop and add to ievent counter.
    Here we assume piety has already added task t to schedule.
    """
    if t.input != timer: # and t.input not in inputs: # do we still need this?
        # always passes the same reader_handler
        # which gets specific handler for this input from piety schedule
        loop.add_reader(t.input, (lambda: reader_handler(t.input)))
    if t.input not in ievent:
        ievent[t.input] = 0
    # if t.input == timer
    # nothing more needed here, piety already added t to schedule
        
def deactivate(t):
    """
    De-activate task t by deleting t.input from loop and ievent counter.
    Here we assume piety has already removed task t from schedule.
    """
    # Only remove t.input from loop when no more tasks in schedule use t.input
    if t.input not in schedule:
        loop.remove_reader(t.input)
        if t.input in ievent:
            del ievent[t.input]

def quit():
    'Exit from Piety event loop'
    global done
    done = True # must reset to False before we can resume

def run(nevents=0): # nevents arg must have same name as in select/eventloop.py
    global maxevents, loop_nevents # global so handle_timeout can see them
    maxevents = ievent[timer] + nevents # ievent includes previous calls to run
    loop_nevents = nevents
    loop.call_soon(timeout_handler) # start recurring timeout
    loop.run_forever()
    loop.close() # does this mean we can't run() from main again?

