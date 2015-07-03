"""
eventloop.py using asyncio as an alternative to select
"""

import asyncio
import datetime
from schedule import schedule, ievent, timer, handler

# create loop here to persist across multiple calls to run()
loop = asyncio.get_event_loop()

# This has to be global in eventloop because piety.tasks() uses it
period = 1.0 # seconds

done = False # used in timeout_handler and also by quit() below
             # does not need to be visible outside this module

def timeout_handler(nevents, maxevents):
    if done or (nevents and ievent[timer] >= maxevents):
        loop.stop()
    else:
        handler(timer)
        loop.call_later(period, timeout_handler, nevents, maxevents)

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
    """
    Run the Piety event loop.
    nevents: number of timer events to process, then exit run loop.
               if nevents not 0, runs even if done==True
             Use default nevents=0 
               to process until done==True or unhandled exception
    """
    resume() # in case an earlier call to run() called quit() and set done=True
    # if nevents not 0, runs even if done==True
    maxevents = ievent[timer] + nevents # ievent includes previous calls to run()
    loop.call_soon(timeout_handler, nevents, maxevents) # start recurring timeout
    loop.run_forever()
    # loop.close() # Not! this would prevent run() from script main() again
