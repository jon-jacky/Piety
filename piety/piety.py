"""
piety.py - Piety scheduler, defines the Task class and run function.  

To run tasks in Piety, import the piety module, create some piety.Task
instances, then call piety.run. More details appear in the docstrings below,
and in the examples in the scripts directory.

Has a main method, python piety.py demonstrates the basics.

This is a platform-dependent module. It uses the select module, so it
must run on a Unix-like host OS (including Linux and Mac OS X).  One
of the select channels is stdin (which I recall does *not* work
in the Windows version of select).
"""

import sys
import datetime
from select import select
from collections import defaultdict, deque, Counter

# Constants used by Task class

def true(): return True # always returns True, can say t0.enabled = piety.true
def false(): return False
    
class Task(object):
    'Task instances are scheduled and invoked by the Piety scheduler.'
    taskno = 0

    def __init__(self, name=None, event=None, handler=None, enabled=true):
        """
        A Task instance identifies a handler, an event, an enabling
        condition, and a name.  The Piety scheduler may
        invoke the handler when the event occurs and the enabling
        condition is True.  Then the handler runs until it returns (or
        yields) control to the scheduler.  There is no preemption.

        This constructor creates a Task object and adds it to
        the collection of scheduled tasks.

        This constructor should always be called with keyword
        arguments. Arguments are:

        name - task name. By default, a unique name is constructed
        of the form tN, where N is a small decimal number.         
        
        event - event which must occur to cause the scheduler to
        invoke the handler.  Defaults to None, meaning the handler is
        never invoked.  In this version the events are the file
        objects watched by the select call in the scheduler's
        event loop, including sys.stdin and possibly others. 
        Another event is timeout, the periodic select timeout event.

        handler - callable object to be invoked by the
        scheduler.  Defaults to None, meaning nothing is called.
        In this version the handler must have no arguments.

        enabled - enabling condition, a Boolean callable object which
        must return True to cause the scheduler to invoke the handler.
        Defaults to a function that always returns True, meaning the
        handler may be invoked whenever the event occurs.
        """
        self.taskno = Task.taskno # unique task ident
        Task.taskno += 1        
        self.name = name if name else 't%d' % self.taskno
        self.handler = handler
        self.event = event
        self.enabled = enabled
        tasks_list.append(self)
        if event:
            schedule[event].append(self)

# Variables and functions for managing tasks

tasks_list = list() # list of tasks in order of creation

def tasks():
    'Display information about all tasks.'

    def oname(obj):
        'Extract informative name from Python object description string.'
        s = str(obj)
        if s.startswith('<function'):
            name = (s.split())[1]
        elif s.startswith('<bound method'):
            name = (s.split())[2]
        elif s.startswith('<open file'):
            name = (s.split())[2]
        else:
            name = s[:15]
        return name.strip("'<>,")

    def ename(e):
        'Handle special case in event name.'

        if e == -1:
            return 'timeout %s s' % period
        else:
            return oname(e)
        
    print """  i  name  enabled              n  event            handler
  -  ----  -------              -  -----            -------"""
    for t in tasks_list:
        print '%3d %5s  %-15s  %5d  %-15s  %-15s' % \
            (t.taskno, t.name, oname(t.enabled), 
             ievent[t.event], ename(t.event), oname(t.handler))

# Variables annd functions used in Piety event loop

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

# key: event, value: list of tasks waiting for event 
schedule = defaultdict(list)

done = False  # can exit on demand

def quit():
    'Exit from Piety event loop'
    global done
    done = True # must reset to False before we can resume
    
def run(nevents=0):
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
                        # Without flush here, char doesn't appear on terminal
                        #  until *next* character is typed at keyboard.
                        # BUT only when handler is invoked here after select
                        # When handler is invoked from simple main loop
                        #  without Piety scheduler, this flush isn't necessary.
                        sys.stdout.flush() # FIXME? investigate problem
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

# Test

def task0(): print 'task 0'
def task1(): print 'task 1'

def main():
    t0 = Task(name='task 0', handler=task0, event=timeout)
    t1 = Task(name='task 1', handler=task1, event=timeout)
    done = False # reset, might be resuming after quit() 
    run(nevents=10) # handle 10 clock ticks and exit
    tasks() # show the tasks

if __name__ == '__main__':
    main()
