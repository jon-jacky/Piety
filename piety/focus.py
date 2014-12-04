"""
focus.py - Manage focus for multiple terminal applications.
           The single stdin/stdout can be multiplexed among several.
"""

# Focus is the task that has console focus:
# the task whose command function is called when input line is complete.
focus = None

def change_focus(new_focus):
  'change console focus to console instance new_focus'
  global focus
  focus = new_focus


class Command(object):
    'Callable command object that can be invoked from the Piety shell'
    
    def __init__(self, console, run, quit, cleanup, successor):
        """
        console - console instance to be invoked by command object
        run - method to call to initialize console 
               when command runs or resumes
        quit - method command calls to quit, we'll monkeypatch this
        cleanup - method to call to clean up console 
               when command exits or suspends
        successor - console instance that gets focus 
               when command exits or suspends
               usually successor will be the pysht shell
        """
        self.console = console
        self.run = run
        def new_quit():
            quit() 
            cleanup()
            change_focus(successor)
        # monkeypatch quit, replace it with new_quit (which calls quit)
        sys.modules[quit.__module__].__dict__[quit.__name__] = new_quit

    def __call__(self):
        change_focus(self.console)
        self.run()
