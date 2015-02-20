"""
job.py - Wrapper for application to provide hooks for job control from Session.
"""

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
        Most arguments are assigned to application callables (fcns or methods).
        In general it is not necessary that these have particular names,
         BUT some of the defaults here do assume they have particular names:
          the ones used in the Command class, so the defaults will work 
          when application is a Command instance, or uses the same method names.
         If application does not use these method names, these defaults 
          will not work, and the arguments must be provided explicitly.
        session - object with a method named stop called at exit for job control.
o          Default: None, this arg not needed if this job runs without job control.
        application - application module or object
          Default: no default, required argument
        startup - callable to call if needed when application starts up or resumes,
           to initialize display or ...  
          Default: None, this argument is not needed for some applications.
        restart - callable to put application in the mode where it handles calls
           to its reader and collects input.
          Default: self.application.restart, the method used in the Command class
        reader - callable that collects input for the application.
           Session assigns Job's reader to Task's handler when Job gets focus.
          Default: self.application.reader, the method used in the Command class
        handler_name - name (a string) of application method that calls 
           application's handler on a chunk of input collected by reader.  
          Default: 'do_command', the method name used in the Command class.
        stopped - callable that returns True when application is about to exit. 
          Default: (lambda: True), which causes application to exit after one cmd.
        cleanup - callable to call if needed when application exits or suspends,
           to clean up display or ... 
          Default: None, this argument is not needed for some applications.
        """
        self.session = session
        self.application = application
        self.startup = startup
        self.restart = restart if restart else self.application.restart
        self.reader = reader if reader else self.application.reader
        self.handler_name = handler_name if handler_name else 'do_command'
        self.do_command_body = getattr(self.application, self.handler_name)
        setattr(self.application,self.handler_name,self.do_command) # monkey patch!
        self.stopped = stopped if stopped else (lambda: True)
        self.cleanup = cleanup
        self.continues = True  # after this, managed by methods in self.session

    def do_command(self):
        'Handle the command, then prepare to collect the next command'
        self.do_command_body() # This is *application* do_command, see above
        if self.stopped():
            self.do_stop()
        elif self.continues and self.restart:
            self.restart()
        else:  # this job does not continue, instead new job takes over
            return  # do not restart this job

    def do_stop(self):
        'Call optional cleanup fcn, then call session job control - if they exist'
        if self.cleanup:
            self.cleanup()
        if self.session:
            self.session.stop()

    def __call__(self):
        'Switch jobs, execute startup function if it exists, then restart reader'
        if self.session:
            self.session.start(self)
        self.run()

    def run(self):
        'Execute startup function if it exists, then restart reader'
        if self.startup:
            self.startup() 
        if self.restart:
            self.restart()

# No main(), any test has to be in another module that imports this one, 
#  to avoid creating a dependency on any particular device or event.
