"""
piety.py - defines Task, Session, schedule, and run (the event loop).
           Imports eventloop used by run.

To run tasks in Piety, import the piety module, create some piety.Task
instances, then call piety.run.  More details appear in the docstrings
below, in the examples in the scripts directory, and in piety.md.
"""

import collections # for deque

# Import the eventloop module for the platform where piety runs
# The eventloop implementation is platform-dependent but its interface is not,
#  so this piety module is platform-independent.
# On Unix-like hosts, we used to import select/eventloop.py
#  Since Python3 we now import asyncio/eventloop.py
import eventloop # for activate, deactivate, to distinguish from same local here

# Other scripts use these identifiers via piety.run() etc.
from eventloop import run, start, stop

# These used to be defined here, continue to say timer not cycle.timer etc.
from cycle import schedule, ievent, timer
import cycle # must use cycle.period, because immutable ...

# Constants used by Task class
def true(): return True # always returns True, can say t0.enabled = piety.true
def false(): return False
    
class Task(object):
    'Task instances are scheduled and invoked by a Piety event loop.'
    taskno = 0

    def __init__(self, name=None, input=None, handler=None, enabled=true):
        """
        A Task instance identifies a handler, an input source, an enabling
        condition, and a name.  A Piety event loop may
        invoke the handler when input is available and the enabling
        condition is True.  Then the handler runs until it returns (or
        yields) control to the event loop.  There is no preemption.

        This initializer creates a Task object and adds it to
        the collection of scheduled tasks.

        This initializer should always be called with keyword
        arguments. Arguments are:

        name - task name. By default, a unique name is constructed
        of the form tN, where N is a small decimal number.         
        
        input - source where data must be available to cause the event loop to
        invoke the handler.  Defaults to None, meaning the handler is
        never invoked.  In this version the inputs are the file-like
        objects watched by the select call in the
        event loop, including sys.stdin and possibly others. 
        Another input is timer, the periodic select timeout input.

        handler - callable object to be invoked by the
        event loop.  Defaults to None, meaning nothing is called.
        In this version the handler must have no arguments.

        enabled - enabling condition, a Boolean callable object which
        must return True to cause the event loop to invoke the handler.
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
        'Add this task to the schedule'
        schedule[self.input].append(self)
        if input not in ievent:
            ievent[input] = 0
        eventloop.activate(self)

    def deactivate(self):
        'Remove this task from the schedule'
        del schedule[self.input].self
        if t.input not in schedule and t.input in ievent:
            del ievent[t.input]
        eventloop.deactivate(self) # only remove if last task with this input

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
            return 'timer %s s' % cycle.period
            #return 'timer  ? s' # placeholder if we can't use period
        else:
            return oname(e)
        
    print("""  i     name  enabled              n  input            handler
  -     ----  -------              -  -----            -------""")
    for t in tasks_list:
        print('%3d %8s  %-15s  %5d  %-15s  %-15s' % \
            (t.taskno, t.name, oname(t.enabled), 
             ievent[t.input], # ievent imported from eventloop
             # '  ???', # placeholder if we can't use ievent
             ename(t.input), oname(t.handler)))

class Session(Task):
    """
    Manage multiple jobs (applications) that use the same input event,in one task.
    """
    # This class was created to support a console terminal session 
    #  that initially runs a Python interpreter, which then starts other jobs.
    # But there is no dependence here on a console terminal or Python interpreter,
    #  so this class might also manage other kinds of sessions and jobs.
    def __init__(self, name=None, input=None, enabled=true):
        """
        Same args as Task __init__ , except no handler.
        Add jobs later, the foreground job's handler becomes the Task handler

        The collection of jobs is a stack implemented by a deque.
        Job on top of stack runs in foreground (has focus), gets input.
        Top of the stack is the right end of the deque at self.jobs[-1]
        """
        # Typically the bottom of the stack is the Python interpreter,
        # and the top of the stack is a job that it started.
        self.jobs = collections.deque()
        self.foreground = None
        super(Session, self).__init__(name=name, input=input, enabled=enabled)

    def start(self, job):
        'Put a new job in the foreground, replace any current job'
        # This is currently the only way to add a job to a Session instance.
        # Typically the old job (if any) is the Python interpreter, which starts the new job.
        # To start a console session, call this with the Python interpreter as the new job.
        if self.foreground:
            self.foreground.replaced = True # replace old job
        self.jobs.append(job)             # add new job
        self.foreground = job             # give it the focus
        self.handler = self.foreground.handler # make its handler this task's handler
        self.foreground.replaced = False # enable new job
        # new foreground job calls its own run() method

    def resume(self):
        'Remove foreground job, resume running preceding job (if any) in foreground'
        # Typically, the preceding job here (if any) is the Python interpreter,
        #  this returns to the interpreter after stopping the job it started.
        # If the current job here is the Python interpreter, this exits session.
        self.jobs.pop()
        if self.jobs:
            self.foreground = self.jobs[-1]
            self.handler = self.foreground.handler
            self.foreground.replaced = False # enable new foreground job
            self.foreground.run()
        # else ... last job exits, its cleanup method has to handle it.

class Job(object):
    'Provide a standard interface to an application that can be used by Session'
    def __init__(self, controller=None, handler=(lambda: ''), # command=None, 
                 startup=(lambda: None), restart=(lambda: None), 
                 cleanup=(lambda: None)):
        """
        All arguments are optional, with defaults

        controller - object or module used for job control, when this
        Job instance is multiplexed with other Jobs that use the same
        event.  Default: None, use when no other jobs contend for the
        same event.  If present, the controller object must have
        start() and resume() mathods.

        handler - callable to read one or more characters to build
        command string.  Takes no arguments and returns a string
        (might be just a single character).  Default returns empty
        string.   Typically, the handler invokes the application 
        on the command, when the command string is complete.

        startup - callable to execute when application starts up or
        resumes, for example to initialize display. Takes a variable
        number of arguments (no arguments is okay).  Default does
        nothing.

        restart - callable to begin another activity cycle in the
        application.  For example, in a command line application,
        print the prompt.  Default does nothing.

        cleanup - callable to run when application exits or suspends,
        for example to clean up display.  Default does nothing.
        """
        self.controller = controller
        self.handler = handler 
        self.startup = startup
        self.restart = restart
        self.cleanup = cleanup
        self.replaced = False 

    def __call__(self, *args, **kwargs):
        """
        Make this Command instance into a callable so it can be invoked by name from Python.
        Give this job focus and Put this job in the foreground and start it.
        """
        if self.controller: # this might be a standalone job with no controller
            self.controller.start(self) # make this the new foreground job
        self.run(*args, **kwargs)

    # Can't merge this into __call__ above because Session resume() also calls it.
    def run(self, *args, **kwargs):
        'Execute startup function if it exists, then restart handler'
        self.startup(*args, **kwargs) 
        self.restart()

    # assign to callback in application 
    def stop(self):
        'This job is done for now.  Clean up, resume previous job if any'
        self.cleanup()
        if self.controller:
            self.controller.resume() 

# Test

def task0(): print('task 0')
def task1(): print('task 1')

def main():
    # We don't want to create these tasks *except* during this test
    # Creates a pair of tasks each time main() is called
    t0 = Task(name='task 0', handler=task0, input=timer)
    t1 = Task(name='task 1', handler=task1, input=timer)
    # we don't need to assign piety.done because we use nevents instead
    run(nevents=10) # handle 10 clock ticks and exit
    tasks() # show the tasks

if __name__ == '__main__':
    main()
