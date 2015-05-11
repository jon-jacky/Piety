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
    def __init__(self, name=None, input=None, enabled=piety.true):
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
