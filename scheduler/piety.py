"""
piety.py - Piety scheduler, defines the Task class and the schedule data structure

To run tasks in Piety, import the piety module, create some piety.Task
instances, then call piety.run.  More details appear in the docstrings
below, and in the examples in the scripts directory.
"""

from collections import defaultdict

# Import the eventloop module for the platform where piety runs
# The eventloop implementation is platform-dependent but its interface is not,
#  so this piety module is platform-independent.
# For Unix-like hosts, arrange to import select/eventloop.py
import eventloop # FIXME? probably better than making scripts import eventloop

# FIXME? other scripts use these identifiers via piety.timeout etc.
from eventloop import timeout, done, ievent, quit 

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
            return 'timeout %s s' % eventloop.period
            #return 'timeout  ? s' # placeholder if we can't use period
        else:
            return oname(e)
        
    print """  i     name  enabled              n  event            handler
  -     ----  -------              -  -----            -------"""
    for t in tasks_list:
        print '%3d %8s  %-15s  %5d  %-15s  %-15s' % \
            (t.taskno, t.name, oname(t.enabled), 
             ievent[t.event], # ievent imported from eventloop
             # '  ???', # placeholder if we can't use ievent
             ename(t.event), oname(t.handler))

# Schedule data structure
# key: event, value: list of tasks waiting for that event 
# Task __init__ puts each new task in this schedule
# (Should that be a separate operation?)
schedule = defaultdict(list)

# so other modules can call piety.run not eventloop.run
def run(nevents=0):
    eventloop.run(schedule, nevents=nevents)

# Test


def task0(): print 'task 0'
def task1(): print 'task 1'

def main():
    # Here timeout, done, run are all imported by piety from eventloop
    t0 = Task(name='task 0', handler=task0, event=timeout)
    t1 = Task(name='task 1', handler=task1, event=timeout)
    done = False # reset, might be resuming after quit() 
    run(nevents=10) # handle 10 clock ticks and exit
    tasks() # show the tasks

if __name__ == '__main__':
    main()
