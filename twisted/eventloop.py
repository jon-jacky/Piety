"""
eventloop.py using Twisted as an alternative to select

The only inputs this eventloop can handle are sys.stdin (via twisted.internet.stdio)
and the timer.

piety module says: 
 import eventloop
 from eventloop import run, quit
 ... then calls eventloop.activate and .deactivate

piety module shares these mutable data structures:
 eventloop.schedule = schedule 
 eventloop.ievent = ievent
 eventloop.timer = timer # immutable, but never reassigned so this works too

application script, for example console_char_tasks module that creates console task
shares this method:
 piety.eventloop.application = console

NOTE: At this time *twisted/eventloop.py* only works with tasks that 
    are triggered by the timeout event, for example in *scripts/embedded*
    and *scripts/eventloop*.  
    But it DOES NOT WORK with tasks that use the standard input, for
    example in *scripts.twisted_eventloop/piety.twisted_eventloop*
    Twisted throws exception for unknown reason.
"""

from twisted.internet import stdio, reactor
from twisted.protocols import basic

# This has to be global in eventloop because piety.tasks() uses it
period = 1

class Console(basic.LineReceiver):
    'Twisted-style handler for input from stdin'

    from os import linesep as delimiter # raw mode - we shouldn't need this

    # Must provide methods with these names (override basic.Linereceiver)

    def connectionMade(self):
        self.setRawMode() # send data to rawDataReceived rather than lineReceived

    def rawDataReceived(self, data): # data are one or more chars, not a line
        # Debug prints - try to track down why this DOES NOT WORK
        #print 'eventloop module, Console object, rawDataRecieved method'
        #print ' self', self
        #print ' application', application
        #print ' application.handler', application.handler
        # These all print the intended output, for example:
        #  application.handler <bound method Command.handle_key of <command.Command object at 0x10acc8350>>
        # Alas, it still doesn't work, Twisted throws exception, reason unknown
        application.handler(data) #  call Piety Session
        ievent[sys.stdin] += 1 # count events
        print 'returned from application.handler, about to exit rawDataRecieved'
        # interval = adjust_interval(t0, interval) # not needed, Twisted handles this
        # select/eventloop.py doesn't do the following - I think quit() handles this
        #if pysh.pexit:
        #    reactor.stop()

done = False # used in Timeout handler and also by quit() below
             # does not need to be visible outside this module

class Timeout(object):
    'Twisted-style timeout handler'

    def __init__(self, nevents):
        # In select/eventloop.py nevents is local arg in piety.run()
        self.nevents = nevents
        # As in select/eventloop.py
        # Allows multiple run() calls, new nevents each time, ievent keeps counting up
        self.maxevents = ievent[timer] + nevents

    def handler(self):
        #print 'done %s, self.nevents %s, ievent[timer] %s, self.maxevents %s' % \
        #     (done,self.nevents,ievent[timer], self.maxevents) # DEBUG
        if done or (self.nevents and ievent[timer] >= self.maxevents):
            reactor.stop()
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
            reactor.callLater(interval, self.handler)

# The eventloop API: activate, deactivate, quit, run

def activate(t):
    pass # nothing more needed here

def deactivate(t):
    pass # nothing more needed here

def quit():
    'Exit from Piety event loop'
    global done
    done = True # must reset to False before we can resume

def run(nevents=0): # nevents arg must have the same name as in select/eventloop.py
    """
    Run the Piety event loop.
    twisted_nevents: number of timer events to process, then exit run loop.
              use default nevents=0 
              to process until done=True or unhandled exception
    """
    #print 'eventloop, beginning run()'
    #print ' application', application
    #print ' application.handler', application.handler
    reactor.callWhenRunning(Timeout(nevents).handler) 
    stdio.StandardIO(Console())
    reactor.run()
