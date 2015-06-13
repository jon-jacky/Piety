"""
piety.py - defines Task, Job, Session, schedule, and run (the event loop).
           Imports eventloop used by run.

To run tasks in Piety, import the piety module, create some piety.Task
instances, then call piety.run.  More details appear in the docstrings
below, in the examples in the scripts directory, and in piety.md.
"""

import collections # for Counter, defaultdict, deque

# Import the eventloop module for the platform where piety runs
# The eventloop implementation is platform-dependent but its interface is not,
#  so this piety module is platform-independent.
# On Unix-like hosts, we usually arrange to import select/eventloop.py
import eventloop

# Other scripts use these identifiers via piety.run() etc.
from eventloop import run, quit

# Schedule data structure
# key, value: input, list of tasks waiting for data at that input
# Task __init__ puts each new task in this schedule, using activate method
schedule = collections.defaultdict(list)

# Count events on each input. key: input, value: number of events on that input
# This item is global so it can be for enabling conditions and handlers.
ievent = collections.Counter()

timer = -1 # indicates timer input, not timeout interval. Differs from any fd.fileno()

# Share mutable data structures with eventloop module
eventloop.schedule = schedule 
eventloop.ievent = ievent
eventloop.timer = timer # immutable, but never reassigned so this works too

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
        self.handler = self.foreground.reader # make its reader this task's handler
        self.foreground.continues = True  # new job continues

    def stop(self):
        'Foreground job says goodbye, stops, new foreground job runs'
        self.jobs.pop()
        if self.jobs:
            self.foreground.continues = False
            self.foreground = self.jobs[-1]
            self.handler = self.foreground.reader
            self.foreground.continues = True
            self.foreground.run()
        # else ... last job exits, its cleanup method has to handle it.

class Job(object):
    """
    Job provides a uniform interface (with known method names) to the application 
    for the Session's job control. Job also uncouples Session's scheduling and job
    control from any particular device or event (such as the terminal). Therefore
    its initializer has to have a lot of arguments to access application methods.
    """
    def __init__(self, session=None, application=None, 
                 startup=None, restart=None, reader=None, handler_name='',
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

        session - object or module with functions or methods named
        start and stop, used for job control.  Default: no default,
        required argument.

        application - application module or object. Default: no
        default, required argument.
        
        startup - callable to call if needed when application starts
        up or resumes, to initialize display or ...  Default: None,
        this argument is not used by some applications.

        restart - callable to put the application in the mode where it
        handles calls to its reader and collects input. Default:
        self.application.restart, the method used in the Command
        class.

        reader - callable that collects input for the application.
        Session assigns Job's reader to Task's handler when Job gets
        focus.  Default: self.application.reader, the method used in
        the Command class.

        handler_name - name (a string) of the application method that
        calls application's handler on a chunk of input collected by
        reader.  Default: 'handler', the method name used in the
        Command class.
        
        stopped - callable that returns True when application is about
        to exit.  Default: (lambda: True), which causes application to
        exit after one cmd.

        cleanup - callable to call if needed when application exits or
        suspends, to clean up display or ...  Default: None, this
        argument is not used by some applications.
        """
        self.session = session
        self.application = application
        self.startup = startup
        self.restart = restart if restart else self.application.restart
        self.reader = reader if reader else self.application.reader
        self.handler_name = handler_name if handler_name else 'handler'
        self.handler_body = getattr(self.application, self.handler_name)
        setattr(self.application,self.handler_name,self.handler) # monkey patch!
        self.stopped = stopped if stopped else (lambda: True)
        self.cleanup = cleanup
        self.continues = True  # after this, managed by methods in self.session

    def handler(self):
        'Handle the command, then prepare to collect the next command'
        self.handler_body() # This is *application* handler, see above
        if self.stopped():
            self.stop()
        elif self.continues and self.restart:
            self.restart()
        else:  # this job does not continue, instead new job takes over
            return  # do not restart this job

    def __call__(self, *args, **kwargs):
        'Switch jobs, execute startup function if it exists, then restart reader'
        self.session.start(self)
        self.run(*args, **kwargs)

    def run(self, *args, **kwargs):
        'Execute startup function if it exists, then restart reader'
        if self.startup:
            self.startup(*args, **kwargs) 
        if self.restart:
            self.restart()

    def stop(self):
        'Call optional cleanup fcn, then call session job control - if they exist'
        if self.cleanup:
            self.cleanup()
        self.session.stop()


# Test

def task0(): print('task 0')
def task1(): print('task 1')

def main():
    # Here timer, done, run are all imported by piety from eventloop
    t0 = Task(name='task 0', handler=task0, input=timer)
    t1 = Task(name='task 1', handler=task1, input=timer)
    done = False # reset, might be resuming after quit() 
    run(nevents=10) # handle 10 clock ticks and exit
    tasks() # show the tasks

if __name__ == '__main__':
    main()
