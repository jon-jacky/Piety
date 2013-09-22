
"""
console.py - skeleton command line application for Piety

Defines a class Console, with a getchar method that gets a single
character typed at the console keyboard, and adds it to a command line
(usually).  When getchar gets a line terminator character, it calls a
command function and passes the command line to it.  Getchar also handles
some editing functions and other control keys (see below).

The getchar method is non-blocking when it is scheduled by the Piety
scheduler.  Other Piety tasks can run while the user is entering the
command line.

To use getchar, the console must have already been put into
single-character mode, by calling the setup function in the terminal
module.  Call the restore function to return to the previous mode.

The default command function simply echoes the command line to the
console display.  A different command function can be passed as an
optional argument to the constructor, so this same class can act as
the front end to any command line application.  The command function
can invoke the Python interpreter itself, so this class can act as
Piety's Python shell.

Editing functions and control keys handled by getchar:
Return, Enter: execute command line by passing it to command function
^H, backspace, delete: remove last character from command line
^L, formfeed: redisplay command line on new line, useful after ^H
^C: raise KeyboardInterrupt, usually exits Piety, returns to Python interpreter
any other key: append character to command line 

Echo and editing are handled here, rather than in the terminal module,
so they can be different for each console instance.  It might be
possible to make different Console subclasses with different getchar
methods that provide different echo and edit behavior.

"""

import sys
import terminal

def echoline(cmdline):
    """
    Print command line on console display.  
    Here command line must be passed parameter.
    """
    print cmdline


class Console(object):
    """
    Skeleton command line application for Piety.  Has a getchar method
    that gets a single character typed at the console keyboard, and
    adds it to a command line (usually).  Schedule getchar from the Piety
    scheduler for non-blocking command input.  When getchar gets a line
    terminator character, it calls a command function and passes the
    command line to it.  We may add command line editing.
    """

    def __init__(self, prompt='piety> ', terminator='\r', echo=True,
                 command=None):
        """
        Creates a Console instance
        prompt - optional argument, prompt string, default is 'piety>'
        terminator - optional argument, default is RETURN '\r'
        echo - optional argument, default is True
        command - optional argument, function to execute command line
          can be any callable that takes one argument, a string
          default just echoes the command line
        """
        self.cmdline = str()
        self.prompt = prompt
        self.terminator = terminator
        self.echo = echo
        self.command = command if command else echoline

    def getchar(self):
        """
        Get character from console keyboard, add to command line
        Execute command line with RET or Enter
        Edit command line with BS or DEL, redisplay with FF or ^L
        Abandon command line, exit to Python interpreter with ^C
        """
        c = terminal.getchar()
        if c == self.terminator: # cmdline does NOT include terminator
            self.do_command()
        elif c in ('\b', '\x7F'): # (backspace, delete) treated the same
            self.cmdline = self.cmdline[:-1] # remove last character
            if self.echo:
                terminal.putstr('^H') # old-timers will recognize this
        elif c == '\f' : # form feed, ^L, redisplay cmdline, useful after ^H
            # no change to cmdline
            terminal.putstr('^L\r\n' + self.prompt + self.cmdline) # on new line
        # raw mode terminal doesn't respond to ^C, must handle here
        elif c == '\x03' : # ascii ETX, ^C, raise exception
            terminal.putstr('^C') # on new line
            terminal.restore() # otherwise traceback looks like a mess
            print
            raise KeyboardInterrupt
        else:
            self.cmdline += c # yes, I know this is inefficient
            if self.echo:
                terminal.putstr(c) # no RETURN - all c go on same line
        return c  # so caller can check for terminator or ...

    def do_command(self):
        """
        Process command line and reinitialize
        """
        terminal.restore() # resume line mode for command output
        print # print command output on new line
        self.command(self.cmdline)
        self.restart()

    def restart(self):
        """
        Initialize: clear command line, print prompt, set single-char mode, 
        """
        self.cmdline = str()
        terminal.putstr(self.prompt) # prompt does not end with \n
        terminal.setup() # resume single character mode

