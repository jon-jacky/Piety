"""
eventloop.py using asyncio as an alternative to select
"""

import asyncio, datetime
from cycle import schedule, handler, ievent, timer, start, stop
import cycle # must use cycle.period, cycle.running, because immutable ...

# create loop here to persist across multiple calls to run()
loop = asyncio.get_event_loop()

# piety eventloop API: activate, deactivate, run

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

# callback for loop.call_soon
def timeout_handler(nevents, maxevents):
    'Recurring timeout, in loop.call_later it rescheduls itself'
    if not cycle.running or (nevents and ievent[timer] >= maxevents):
        loop.stop()
    else:
        handler(timer)
        loop.call_later(cycle.period, timeout_handler, nevents, maxevents)

def run(nevents=0): # nevents arg must have same name as in select/eventloop.py
    """
    Run the Piety event loop.
    nevents: number of timer events to process, then exit run loop.
     If nevents not 0, runs even if running==False
     Use default nevents=0 to process until running==False or unhandled exception
    """
    start()
    # ievent includes previous calls to run()
    maxevents = ievent[timer] + nevents 
    loop.call_soon(timeout_handler, nevents, maxevents) # start recurring timeout
    loop.run_forever()
    # loop.close() # Not! this would prevent run() from script main() again
