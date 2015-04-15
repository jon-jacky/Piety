"""
commandline.py - do-nothing wrapper for command line applications
                  to interface with Job class
"""

# quit and echo are copied from command.py, could be omitted here if we merge 

quit = False

def echo(command):
    'Default handler, print command on console, q exits without printing'
    global quit
    if command == 'q':
        quit = True
    else:
        print command

class CommandLine(object):
    """
    Wrapper for command line applications to interface with the Job class.
    Use instead of the Command class, where the caller or environment already 
    collects the completed command line for the application.
    Unlike the Command class, this provides no command line editing or history. It
    merely accepts an already-formed command line and passes it to the application.
    """
    def __init__(self, prompt='>', handler=echo): 
        # no reader, no trailing blank on prompt because raw_input adds it.
        """
        Creates all the attributes used by Job, same as Command __init__.
        Prompt and handler arguments are the same as in Command __init__.
        But no reader argument here.  Instead, reader method is already built in,
        it takes a string argument instead of collecting the cmd line char-by-char.
        """
        self.prompt = prompt # string to prompt for command 
        self.handler_body = handler # callable that executes command string
        self.command = '' # command string 

    def reader(self, command):
        'command is the command line string that the handler will process'
        self.command = command
        self.handler()

    def handler(self):
        self.handler_body(self.command)

    # Like Command restart, but simplified - no editing point, no single-char mode.
    def restart(self):
        'Clear command string, print command prompt'
        self.command = str()
        print self.prompt, # prompt does not end with \n

# Test

c = CommandLine()

def main():
    global quit
    quit = False # earlier invocation might have set it True
    # default handler echo sets quit=True when command='q'
    while not quit:
        c.restart() # prints prompt with no trailing blank
        command = raw_input() # adds trailing blank after prompt
        c.reader(command)

if __name__ == '__main__':
    main()
