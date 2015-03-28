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

# No main(), any test has to be in another module that imports this one, 
#  to avoid creating a dependency on any particular device or event.
