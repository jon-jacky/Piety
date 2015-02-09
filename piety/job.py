"""
job.py - Wrapper for application to provide hooks for job control from Session.
"""

class Job(object):
    """
    Job provides a uniform interface to the application for the
    Session's job control.  Job also uncouples Session's scheduling and job
    control from any particular device or event.  Therefore its initializer
    has a lot of arguments to access application functions.
    """
    def __init__(self, application=None, startup=None, restart=None, reader=None, 
                 replaced=None, stopped=None, cleanup=None, suspend=None):
        """ 
        application - required argument, application object.
          application must have a method named do_command that calls 
           application's handler on a chunk of input collected by reader.  
        startup - optional function to call when application starts up or resumes.
        restart - optional function to put application in the mode where it
          handles calls to reader and collects input.
        reader - required function to call to collect input for the application.
          Session assigns Job's reader to Task's handler when Job gets focus.
        replaced - required function called by do_command that returns True 
           when a new application is about to run, replacing the current job.
        stopped - required function called by do_command that returns True 
           when application is about to exit. 
          When stopped is True, this job executes cleanup, then suspend
        cleanup - optional function to call when application exits or suspends.
          Called after stop (above) returns True
        suspend - optional job control function to put this job
          in the background. Used when running other jobs. Runs after cleanup.
        """
        self.application = application
        self.startup = startup
        self.restart = restart
        self.reader = reader
        self.do_command_body = application.do_command
        application.do_command = self.do_command
        self.replaced = replaced
        self.stopped = stopped
        self.cleanup = cleanup
        self.suspend = suspend

    def do_command(self):
        'Handle the command, then prepare to collect the next command'
        self.do_command_body() # This is *application* do_command, see above
        if self.stopped():
            self.do_stop()
        elif not self.replaced() and self.restart:
            self.restart()
        else:
            return

    def do_stop(self):
        'Call optional cleanup fcn, then call suspend callback - if they exist'
        if self.cleanup:
            self.cleanup()
        if self.suspend:
            self.suspend()

    def __call__(self):
        'Execute startup function if it exists, then restart reader'
        if self.startup:
            self.startup() 
        if self.restart:
            self.restart()

# Test has to be in another module that imports this one, 
#  to avoid creating a dependency on any particular device or event
