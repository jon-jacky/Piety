"""
session.py - Manage multiple jobs (applications) in one task.

Defines Session class, a subclass of Task.

Usually all applications that get input from the same source run in a
single task.  Session multiplexes the input among them by selecting
one job at a time to run in the foreground.

Example: shell, editor, etc. all get input from keyboard (stdin).
They are multiple jobs in one console session (a task); only one job at
a time runs in the foreground.
"""

import piety
import collections

class Session(piety.Task):
    """
    Manage multiple jobs (applications) that use the same input event,in one task.
    The collection of jobs is a stack implemented by a deque.
    Job on top of stack runs in foreground (has focus), gets input.
    Top of the stack is the right end of the deque at self.jobs[-1]
    """
    def __init__(self, name=None, event=None, enabled=piety.true):
        """
        Same args as Task __init__ , except no handler.
        Add jobs later, the foreground job's handler becomes the Task handler
        """
        self.jobs = collections.deque()
        super(Session, self).__init__(name=name, event=event, 
                                      enabled=enabled)

    # run() the first job before piety.run()
    def run(self, job):
        'Add a new job, put it in the foreground, run it'
        self.jobs.append(job)
        self.foreground = job
        self.run_foreground()

    def run_foreground(self):
        'Initialize the foreground job, then prepare to accept input'
        self.handler = self.foreground.reader
        self.foreground() # invokes its command.__call__ 

    def stop(self):
        'Foreground job says goodbye, stops, new foreground job runs'
        self.jobs.pop()
        if self.jobs:
            self.foreground = self.jobs[-1]
            self.run_foreground()
        # else ... last job exits, its cleanup method has to handle it.
