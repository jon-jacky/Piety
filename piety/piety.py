"""
piety.py - Piety scheduler, defines the Task class and run function.  

To run tasks in Piety, import the piety module, create some piety.Task
instances, then call piety.run. More details appear in the docstrings below,
and in the examples in the samples directory.

This is a platform-dependent module. It uses the select module, so it
must run on a Unix-like host OS (including Linux and Mac OS X).  One
of the select channels is stdin (which I recall does *not* work
in the Windows version of select).

"""

import sys
import datetime
import terminal
from select import select

class Task(object):
    """
    Task instances are scheduled and invoked by the Piety scheduler.
    """
    taskno = 0

    def __init__(self, name=None, handler=None, event=None, guard=None):
        """
        A Task instance identifies a handler, an event, a guard,
        and an optional name.  The Piety scheduler may invoke the
        handler when the event occurs and the guard is True.  Then the
        handler runs until it returns (or yields) control to the
        scheduler.  There is no preemption.

        This constructor creates a Task object also adds it to to
        tasks, the collection of Task objects eligible to be
        scheduled.

        This constructor should always be called with keyword
        arguments. Arguments are:

        name - task name. By default, a unique name is constructed
        of the form task_N, where N is a small decimal number.         
        
        handler - callable object to be invoked by the
        scheduler.  Defaults to None, meaning nothing is called.
        In this version the handler must have no arguments.

        event - event which must occur to cause the scheduler to
        invoke the handler.  Defaults to None, meaning the handler is
        never invoked.  In this version the events are the file
        objects watched by the select call in the scheduler's
        event loop, including sys.stdin and possibly others. 
        Another event is timeout, the periodic select timeout event

        guard - Boolean callable object which must return True to
        cause the scheduler to invoke the handler.  Defaults to a
        callable that always returns True, meaning the handler may be
        invoked whenever the event occurs.
        """
        self.taskno = Task.taskno # unique task ident
        Task.taskno += 1        
        self.name = name if name else 'task_%d' % self.taskno
        self.handler = handler
        self.event = event
        self.guard = guard if guard else (lambda: True)
        if event in tasks:
            tasks[event] += [ self ]
        else:
            tasks[event] = [ self ]


tasks = dict() # { event : list of tasks waiting for that event }
inputs = [sys.stdin] # could add to this list
#outputs = [sys.stdout] # causes run loop to exit without handling other events
outputs = [] # FIXME? for now [sys.stdout] doesn't work
exceptions = []
timeout = -1 # timeout EVENT not interval.  different from any fd.fileno()

# counts events of all types, must be global so handlers can use it
ievent = 0
done = False  # for exit

def exit():
    """ 
    exit from Piety event loop
    """
    global done
    done = True

def run(period=1.000,nevents=0):
    """
    Run the Piety event loop
    period: event loop period, default 1 sec
    nevents: number of events (of any kind) to process
              default nevents=0 processes forever
    """
    global ievent # must be global so tasks can use it
    maxevents = ievent + nevents # when to stop
    interval = period # timeout INTERVAL in seconds, select argument
    while not done and not nevents or ievent < maxevents:
        # Python select doesn't assign time remaining to timeout argument
        # so we have to time it ourselves
        t0 = datetime.datetime.now()
        inputready,outputready,exceptready = select(inputs,outputs,exceptions,
                                                    interval)
        # inputs
        for fd in inputready:
            if fd in tasks:
                for t in tasks[fd]:
                    if t.guard():
                        t.handler()
            else:
                s = fd.readline() # works on stdin, fd.read() hangs
                print 'unhandled input from fd %s: %s' % (fd, s)
            
            # Make sure timeout events occur periodically even if input appears
            # adjust timeout for nearly-constant interval between timeout events
            # despite variable time spent waiting for input and processing it
            t1 = datetime.datetime.now()
            dt = t1 - t0
            dt_sec = dt.seconds + 0.000001*dt.microseconds
            interval = interval - dt_sec # should never be negative ...
            interval = interval if interval > 0.0 else period # ... but ...

        # periodic timeout if no input
        if not (inputready or outputready or exceptready): 
            if timeout in tasks:
                for t in tasks[timeout]:
                    if t.guard():
                        t.handler()
            else:
                pass # if no timeout handler, just continue
            interval = period # if we got here, full period must have elapsed

        # terminal.putstr(' interval %s ' % interval) # DEBUG check adjustment
        ievent += 1

