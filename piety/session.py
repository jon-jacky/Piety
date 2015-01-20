"""
session.py - Define Session class, a subclass of Task 
               that manages multiple applications (jobs) in one task.
              Usually all applications that get input from the same source
               run in a single task.  Session multiplexes the input among them
                by selecting one job at a time to run in the foreground.
             Example: shell, editor, etc. all get input from keyboard (stdin).
               so they are multiple jobs in one task.
"""

import piety
import collections

class Session(piety.Task):
    """
    In one task, manage jobs (applications) that use the same input event
    The collection of jobs is a stack implemented by a deque.
    Job on top of stack runs in foreground (has focus), gets input.
    Top of the stack is the right end of the deque at self.jobs[-1]
    Typical scenario:
      start session, stack is empty
      push shell job on stack and run it
      repeat:
        shell command to start application job pushes it on stack and runs it
        application exits, pop stack and resume running shell job
      shell job exits, pop stack
      stack is empty, exit session
    So the stack usually just holds one or two items
     but application could command another application to start: push and run
    After an application exits, its job remains in Python with all its state
     (though not on the job stack) so it can easily be pushed and run again
    The purpose of the Session class: an application need not know or assume
     which application will resume when it exits - this class keeps track.
    """
    def __init__(self, name=None, event=None, job=None, enabled=piety.true):
        """
        Same args as Task __init__ , except replace handler with job
        The foreground job's handler becomes the Task handler
        """
        self.jobs = collections.deque([job])
        self.foreground = self.jobs[-1] if self.jobs else None
        super(Session, self).__init__(name=name, event=event, 
                                      handler=self.foreground.handler, 
                                      enabled=enabled)

    def run(self, job):
        'Add a new job, put it in the foreground, run it'
        self.jobs.append(job)
        self.foreground = job
        self.run_foreground()

    def run_foreground(self):
        'Initialize the foreground job, then prepare to accept input'
        self.handler = self.foreground.handler
        self.foreground() # invokes its command.__call__ 

    def handle_key(self, key):
        'Pass key to foreground handle_key'
        self.foreground.handle_key(key)

    def stop(self):
        'Foreground job says goodbye, stops, new foreground job runs'
        self.jobs.pop()
        if self.jobs:
            self.foreground = self.jobs[-1]
            self.run_foreground()
        # else:
        #   exit from piety scheduler, return to underlying python

    
