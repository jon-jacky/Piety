"""
eventloop.py using asyncio as an alternative to select
"""

import asyncio
import datetime
from schedule import schedule, ievent, timer, handler

loop = asyncio.get_event_loop()

t0 = datetime.datetime.now()

# This has to be global in eventloop because piety.tasks() uses it
period = 1.0 # seconds

done = False # used in timeout_handler and also by quit() below
             # does not need to be visible outside this module

# FIXME?  Couldn't these be args to timeout_handler instead of global?
loop_nevents = 0  # 0 means run forever, may be reassigned by run() below
maxevents    = 0  # maxevents includes events from previous calls to run()

def timeout_handler():
    #print 'done %s, loop_nevents %s, ievent[timer] %s, maxevents %s' % \
    #     (done,loop_nevents,ievent[timer], maxevents) # DEBUG
    if done or (loop_nevents and ievent[timer] >= maxevents):
        loop.stop()
        # We also use pysh.exit to stop, in Console lineReceived handler
    else:
        handler(timer)
        loop.call_later(period, timeout_handler)

# piety eventloop API: activate, deactivate, quit, run

def activate(t):
    """
    Activate task t by registering t.input with loop and add to ievent counter.
    Here we assume piety has already added task t to schedule.
    """
    if t.input != timer:
        loop.add_reader(t.input, (lambda: handler(t.input)))
        
def deactivate(t):
    """
    De-activate task t by deleting t.input from loop and ievent counter.
    Here we assume piety has already removed task t from schedule.
    Only remove t.input from loop when no more tasks in schedule use t.input
    """
    if t.input not in schedule:
        loop.remove_reader(t.input)

def quit():
    'Exit from Piety event loop'
    global done
    done = True # must reset to False before we can resume

def resume():
    'Resume Piety event loop'
    global done
    done = False

def run(nevents=0): # nevents arg must have same name as in select/eventloop.py
    global maxevents, loop_nevents # global so handle_timeout can see them
    maxevents = ievent[timer] + nevents # ievent includes previous calls to run
    loop_nevents = nevents
    loop.call_soon(timeout_handler) # start recurring timeout
    loop.run_forever()
    # loop.close() # FIXME this means we can't run() from script main() again

