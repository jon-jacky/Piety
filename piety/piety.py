"""
piety.py - Piety scheduler
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
        Another event is timeout_event, the periodic select timeout event

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
timeout_event = -1

# counts events of all types, must be global so handlers can use it
ievent = 0

def run(timeout_interval=1,nevents=0):
    """
    Run the Piety event loop
    timeout_interval: determines event loop period, default 1 sec
    nevents: number of events (of any kind) to process
              default nevents=0 processes forever
    """
    global ievent # must be global so tasks can use it
    maxevents = ievent + nevents # when to stop
    while not nevents or ievent < maxevents:
        inputready,outputready,exceptready = select(inputs,[],[],
                                                    timeout_interval)
        # stdin
        for fd in inputready:
            if fd == sys.stdin:
                for t in tasks[sys.stdin]:
                    if t.guard():
                        t.handler()

        # periodic timeout
        if not (inputready or outputready or exceptready): 
            for t in tasks[timeout_event]:
                    if t.guard():
                        t.handler()        

        ievent += 1

