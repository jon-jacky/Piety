"""
job.py - Defines Job, subclass of Command with hooks for job control with Session.
          Job class provides a uniform API for terminal applications for Session.
          Enables Session to manage several terminal jobs in a single Piety task.
"""

import terminal
import command

class Job(command.Command):
    def __init__(self, startup=None, prompt='> ', 
                 reader=terminal.getchar , handler=command.echo, 
                 stopcmd='q', cleanup=None, suspend=None):
        """
        All arguments are optional, with defaults
        startup - function to call when application starts up or resumes
           for example to initialize screen or ...
          After that, system then prints the command prompt.
          Default does nothing more than print the command prompt.
          This function gets assigned to this object's __call__ method
        prompt - Prompt string that appears at the start of each line
          Default is '> '
        reader - function to call to read char(s) to build command string
          Default is terminal.getchar, could also read/process multichar sequence
        handler - function to execute command
          Can be any callable that takes one argument, a string.
          Default just echoes the command.
        stopcmd - command string for function in application to be executed
          by .handler (above) to exit or suspend. After that, application 
          executes cleanup (below), then job control may execute suspend(below)
          Default is 'q'.
        cleanup - application function to call when application 
          exits or suspends for example to clean up screen or ...
          Called after executing stopcmd (above), default does nothing more
        suspend - callback function from job control to put this job
          in the background. Used when running other jobs. Runs after cleanup.
        """
        self.startup = startup
        self.stopcmd = stopcmd
        self.cleanup = cleanup
        self.suspend = suspend
        super(Job, self).__init__(prompt=prompt, reader=reader, handler=handler)

    def do_command(self):
        'Handle the command, then prepare to collect the next command'
        terminal.set_line_mode() # resume line mode for command output
        print # print command output on new line
        if '.run(' in self.command: # HACK .run( is from job control in session.py
            self.handler(self.command) # *not* followed by restart
        elif self.command == self.stopcmd:
            self.do_stop()
        else:
            self.handler(self.command)
            self.restart()

    def do_stop(self):
        """
        Call handler for stopcmd, 
        then call optional cleanup fcn, then call suspend callback - if they exist
        """
        self.handler(self.stopcmd)        
        if self.cleanup:
            self.cleanup()
        if self.suspend:
            self.suspend()

    def __call__(self):
        'Execute startup function if it exists, then restart command line'
        if self.startup:
            self.startup()
        self.restart()

    def handle_C_d(self):
        '^D: stop if command string is empty, otherwise delete character'
        if not self.command:
            terminal.set_line_mode()
            print('^D') # advance line too
            if self.stopcmd:
                self.do_stop()
        else:
            self.delete_char() # requires display terminal

    # Many other methods Commmand are invoked via Command keymap


# Test

c = Job()

def main():
    command.quit = False # earlier invocation might have set it True
    c()
    while not command.quit:
        # No need to test new_command and call c.restart - Job handles that
        # default reader terminal.getchar can't handle multi-char control seqs
        #  like keyboard.up, down, right, left - use ^P ^N ^F ^B instead
        c.reader()

if __name__ == '__main__':
    main()
