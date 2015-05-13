"""
eventloop.py using Twisted 

piety module says: 
 import eventloop
 from eventloop import run, quit
 ... then calls eventloop.activate and .deactivate

piety module shares these mutable data structures:
 eventloop.schedule = schedule 
 eventloop.ievent = ievent
 eventloop.timer = timer # immutable, but never reassigned so this works too
"""

from twisted.internet import stdio, reactor
from twisted.protocols import basic

class Console(basic.LineReceiver):
    'Twisted-style handler for input from stdin'

    from os import linesep as delimiter # raw mode - we shouldn't need this

    # Must provide methods with these names (override basic.Linereceiver)

    def connectionMade(self):
        self.setRawMode() # send data to rawDataReceived rather than lineReceived
        jobs.pysh() # start the first Piety job, begin prompting

    def rawDataReceived(self, data): # data are one or more chars, not a line
        console.handler(data) #  call Piety Session
        piety.ievent[sys.stdin] += 1 # count events
        # interval = adjust_interval(t0, interval) # not needed, Twisted handles this
        if pysh.pexit:
            reactor.stop()

class Timeout(object):
    'Twisted-style timeout handler'

    def __init__(self):
        self.period = 1 # second, same as embedded script.
        self.nevents = 10 # same as embedded script

    def handler(self):
        if False and piety.ievent[piety.timer] == self.nevents:
            # Now we use pysh.exit to stop, in Console lineReceived handler
            reactor.stop()
        else:
            # handle scheduled timeout events
            if piety.timer in piety.schedule:
                for t in piety.schedule[piety.timer]:
                    if t.enabled():
                        t.handler()
            else:
                pass # if no timeout handler, just continue
            # count events and schedule next timeout
            piety.ievent[piety.timer] += 1
            interval = self.period # if we got here, full interval has elapsed
            reactor.callLater(interval, self.handler)

# The eventloop API: activate, deactivate, quit, run

def activate(t):
    pass # nothing more needed here

def deactivate(t):
    pass # nothing more needed here

done = False # used by quit() below, does not need to be visible outside this module

def quit():
    'Exit from Piety event loop'
    global done
    done = True # must reset to False before we can resume

def run(nevents=0):
    """
    Run the Piety event loop.
    nevents: number of timer events to process, then exit run loop.
              use default nevents=0 
              to process until done=True or unhandled exception
    """
    reactor.callWhenRunning(Timeout().handler) 
    stdio.StandardIO(Console())
    reactor.run()
