"""
piety.py - Piety scheduler, defines the Task class and the schedule data structure

To run tasks in Piety, import the piety module, create some piety.Task
instances, then call piety.run.  More details appear in the docstrings
below, and in the examples in the scripts directory.
"""

from collections import Counter, defaultdict

# Import the eventloop module for the platform where piety runs
# The eventloop implementation is platform-dependent but its interface is not,
#  so this piety module is platform-independent.
# For Unix-like hosts, arrange to import select/eventloop.py
import eventloop

# Other scripts use these identifiers via piety.run() etc.
from eventloop import run, quit

# Schedule data structure
# key, value: input, list of tasks waiting for data at that input
# Task __init__ puts each new task in this schedule, using activate method
schedule = defaultdict(list)

# Count events on each input. key: input, value: number of events on that input
# This item is global so it can be for enabling conditions and handlers.
ievent = Counter()

timer = -1 # indicates timer input, not timeout interval. Differs from any fd.fileno()

# Share mutable data structures with eventloop module
eventloop.schedule = schedule 
eventloop.ievent = ievent
eventloop.timer = timer # immutable, but never reassigned so this works too

# Constants used by Task class

def true(): return True # always returns True, can say t0.enabled = piety.true
def false(): return False
    
class Task(object):
    'Task instances are scheduled and invoked by the Piety scheduler.'
    taskno = 0

    def __init__(self, name=None, input=None, handler=None, enabled=true):
        """
        A Task instance identifies a handler, an input source, an enabling
        condition, and a name.  The Piety scheduler may
        invoke the handler when input is available and the enabling
        condition is True.  Then the handler runs until it returns (or
        yields) control to the scheduler.  There is no preemption.

        This constructor creates a Task object and adds it to
        the collection of scheduled tasks.

        This constructor should always be called with keyword
        arguments. Arguments are:

        name - task name. By default, a unique name is constructed
        of the form tN, where N is a small decimal number.         
        
        input - source where data must be available to cause the scheduler to
        invoke the handler.  Defaults to None, meaning the handler is
        never invoked.  In this version the inputs are the file-like
        objects watched by the select call in the scheduler's
        event loop, including sys.stdin and possibly others. 
        Another input is timer, the periodic select timeout input.

        handler - callable object to be invoked by the
        scheduler.  Defaults to None, meaning nothing is called.
        In this version the handler must have no arguments.

        enabled - enabling condition, a Boolean callable object which
        must return True to cause the scheduler to invoke the handler.
        Defaults to a function that always returns True, meaning the
        handler may be invoked whenever data is available at the input.
        """
        self.taskno = Task.taskno # unique task ident
        Task.taskno += 1        
        self.name = name if name else 't%d' % self.taskno
        self.handler = handler
        self.input = input
        self.enabled = enabled
        tasks_list.append(self) # FIXME? redundant with schedule
        # FIXME? implicitly activate every task on creation - good idea?
        self.activate()

    def activate(self):
        schedule[self.input].append(self)
        eventloop.activate(self) # for select, just adds t.input to select inputs

    def deactivate(self):
        del schedule[self.input].self
        eventloop.deactivate(self) # careful, only remove if last task with this input

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
        'Handle special case in input name.'

        if e == timer:
            return 'timer %s s' % eventloop.period
            #return 'timer  ? s' # placeholder if we can't use period
        else:
            return oname(e)
        
    print """  i     name  enabled              n  input            handler
  -     ----  -------              -  -----            -------"""
    for t in tasks_list:
        print '%3d %8s  %-15s  %5d  %-15s  %-15s' % \
            (t.taskno, t.name, oname(t.enabled), 
             ievent[t.input], # ievent imported from eventloop
             # '  ???', # placeholder if we can't use ievent
             ename(t.input), oname(t.handler))


# Test

def task0(): print 'task 0'
def task1(): print 'task 1'

def main():
    # Here timer, done, run are all imported by piety from eventloop
    t0 = Task(name='task 0', handler=task0, input=timer)
    t1 = Task(name='task 1', handler=task1, input=timer)
    done = False # reset, might be resuming after quit() 
    run(nevents=10) # handle 10 clock ticks and exit
    tasks() # show the tasks

if __name__ == '__main__':
    main()
