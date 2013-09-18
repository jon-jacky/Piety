"""
piety.py - Piety scheduler, defines the Task class and run function.  

To run tasks in Piety, import the piety module, create some Task
instances, then call run. More details appear in the docstrings below,
and in the examples in the samples directory.

This version of the scheduler uses the select module, so it must run
on a Unix-like host OS (including OS X).  

"""

import sys
from select import select

class Task(object):
    """
    Task instances are scheduled and invoked by the Piety scheduler.
    """
    taskno = 0

    def __init__(self, name=None, handler=None, event=None, guard=None):
        """
        A Task instance is defined by a handler, an event, a guard,
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
timeout = -1 # different from any fd.fileno()

# counts events of all types, must be global so handlers can use it
ievent = 0

def run(period=1,nevents=0):
    """
    Run the Piety event loop
    period: event loop period, default 1 sec
    nevents: number of events (of any kind) to process
              default nevents=0 processes forever
    """
    global ievent # must be global so tasks can use it
    maxevents = ievent + nevents # when to stop
    while not nevents or ievent < maxevents:
        inputready,outputready,exceptready = select(inputs,outputs,exceptions,
                                                    period)
        # inputs
        for fd in inputready:
            if fd in tasks:
                for t in tasks[fd]:
                    if t.guard():
                        t.handler()
            else:
                s = fd.readline() # works on stdin, fd.read() hangs
                print 'unhandled input from fd %s: %s' % (fd, s)

        # periodic timeout
        if not (inputready or outputready or exceptready): 
            if timeout in tasks:
                for t in tasks[timeout]:
                    if t.guard():
                        t.handler()
            else:
                pass # if no timeout handler, just continue

        ievent += 1

