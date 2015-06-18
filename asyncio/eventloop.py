"""
eventloop.py using asyncio as an alternative to select
"""

import sys
import asyncio

### asyncio machinery

loop = asyncio.get_event_loop()

### piety machinery

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
        # count events and schedule next timeout
        ievent[timer] += 1
        interval = period # if we got here, full interval has elapsed
        loop.call_later(interval, timeout_handler)

### piety eventloop API: activate, deactivate, quit, run

def activate(t):
    pass # nothing more needed here

def deactivate(t):
    pass # nothing more needed here

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

