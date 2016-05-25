"""
piety.py - defines Task, Job, Session, schedule, and run (the event loop).
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

        This constructor creates a Task object and adds it to
        the collection of scheduled tasks.

        This constructor should always be called with keyword
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
    The collection of jobs is a stack implemented by a deque.
    Job on top of stack runs in foreground (has focus), gets input.
    Top of the stack is the right end of the deque at self.jobs[-1]
    """
    def __init__(self, name=None, input=None, enabled=true):
        """
        Same args as Task __init__ , except no handler.
        Add jobs later, the foreground job's handler becomes the Task handler
        """
        self.jobs = collections.deque()
        self.foreground = None
        super(Session, self).__init__(name=name, input=input, enabled=enabled)

    def start(self, job):
        'Put job in the foreground, prepare to run it'
        # called from new job's __call__ method which calls its own run method
        if self.foreground:
            self.foreground.continues = False # previous job does not continue
        self.jobs.append(job)             # add new job
        self.foreground = job             # give it the focus
        self.handler = self.foreground.handler # make its handler this task's handler

    def stop(self):
        'Foreground job says goodbye, stops, new foreground job runs'
        self.jobs.pop()
        if self.jobs:
            self.foreground = self.jobs[-1]
            self.handler = self.foreground.handler
            self.foreground.continues = True
            self.foreground.run()
        # else ... last job exits, its cleanup method has to handle it.

class Job(object):
    """
    Job provides a uniform interface for job control (with known method names) 
    to an application - it provides standard hooks to start (or restart), then to
    stop (or pause) the application, in addition to just handling events.
    Therefore its initializer has to have a lot of arguments to access
    application methods.  This interface (these methods) make it
    possible for a job controller facility (such as the Session class, above) to
    manage several (or many) applications, including multiplexing events
    among several applications.  A job controller can be assigned to the (optional)
    session argument.
    """
    def __init__(self, application=None, controller=None, 
                 startup=None, restart=None, handler=None, 
                 stopped=None, cleanup=None):
        """ 
        The values assigned to most arguments are application
        callables (functions or methods).

        In general it is not necessary that the application callables have
        particular names, BUT some of the defaults here do assume they
        have particular names: the same names used in the Command class, so
        the defaults will work when the application is a Command
        instance, or uses the same method names.  If the application
        does not use these method names, these defaults will not work,
        and the arguments must be provided explicitly.

        application - application module or object. No default,
        this is a required argument.

        controller - object or module with functions or methods named
        start and stop, used for job control, when this Job instance 
        is multiplexed with other Jobs that use the same event.
        Default: None, use when this Job instance is a task on its own,
        with no other jobs contending for the same event.

        startup - callable to call if needed when application starts
        up or resumes, to initialize display or ...  Default: None,
        this argument is not used by some applications.

        restart - callable to put the application in the mode where it
        handles calls to its handler and collects input. Default:
        self.application.restart, the method used in the Command
        class.

        handler - callable that collects an input element for the application
        (for example, a single character or single keycode).
        Controller cam assign Job's handler to Task's handler when Job gets
        focus.  Default: self.application.handler, the method used in
        the Command class.        

        stopped - callable that returns True when application is about
        to exit.  Default: (lambda: True), which causes application to
        exit after one command.

        cleanup - callable to call if needed when application exits or
        suspends, to clean up display or ...  Default: None, this
        argument is not used by some applications.
        """
        self.application = application
        self.controller = controller
        self.startup = startup
        self.restart = restart if restart else self.application.restart
        self.handler = handler if handler else self.application.handler
        self.stopped = stopped if stopped else (lambda: True)
        self.cleanup = cleanup
        # self.continues is not equivalent to (not self.stopped())
        # because it can be assigned False by job controller when new job takes over,
        # for example see Session start() method above.
        self.continues = True
        # Assign callback in application so this Job can respond to application exit
        self.application.job_control_callback = self.stop_or_restart

    def stop_or_restart(self):
        'Respond to application, assign this method to callback in application'
        if self.stopped():
            self.stop()
        elif self.continues and self.restart:
            self.restart()
        else:  # this job does not continue, instead new job takes over
            return  # do not restart this job

    def __call__(self, *args, **kwargs):
        """
        Makes each job instance into a callable so it can be invoked by name from Python.
        Switch jobs, execute startup function if it exists, then restart handler
        """
        if self.controller:
            self.controller.start(self)
        self.continues = True
        self.run(*args, **kwargs)

    def run(self, *args, **kwargs):
        'Execute startup function if it exists, then restart handler'
        if self.startup:
            self.startup(*args, **kwargs) 
        if self.restart:
            self.restart()

    def stop(self):
        'Call optional cleanup fcn, then call job control - if they exist'
        if self.cleanup:
            self.cleanup()
        self.continues = False
        if self.controller:
            self.controller.stop()

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
