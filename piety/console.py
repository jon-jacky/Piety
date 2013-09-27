
"""
console.py - skeleton command line application for Piety

Defines a class Console, with a getchar method that gets a single
character typed at the console keyboard, and adds it to a command line
(usually).  When getchar gets a line terminator character, it calls a
command function and passes the command line to it.  Getchar also
handles some editing functions and other control keys (see below).

The default command function simply echoes the command line to the
console display.  A different command function can be passed as an
optional argument to the constructor, so this same class can act as
the front end to any command line application.  The command function
can invoke the Python interpreter itself, so this class can act as
Piety's Python shell.

The getchar method is non-blocking when it is scheduled by the Piety
scheduler.  Other Piety tasks can run while the user is entering the
command line.

Before calling the getchar method, put the console instance in
single-character mode by calling its restart method.  The console
itself restores normal mode when it exits (in response to ^C or ^D).

This module is platform independent.  It uses the platform-dependent
terminal module to set and restore terminal characteristics and to
read and write to the terminal.

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

# Print regrets when ^D but no self.exit
noexit = 'No exit function defined, type ^C for KeyboardInterrupt'


class Console(object):
    """
    Skeleton command line application for Piety.  Has a getchar method
    that gets a single character typed at the console keyboard, and
    adds it to a command line (usually).  Schedule getchar from the Piety
    scheduler for non-blocking command input.  When getchar gets a line
    terminator character, it calls a command function and passes the
    command line to it.  A few control characters do command line editing.
    """

    def __init__(self, prompt='piety> ', terminator='\r', echo=True,
                 command=None, exiter=None):
        """
        Creates a Console instance
        prompt - optional argument, prompt string, default is 'piety>'
        terminator - optional argument, default is RETURN '\r'
        echo - optional argument, default is True
        command - optional argument, function to execute command line
          can be any callable that takes one argument, a string
          default just echoes the command line
        exit_fn - optional argument, function to execute in response to ^D key.
          default merely prints a line advising ^C to interrupt.
        """
        self.cmdline = str()
        self.prompt = prompt
        self.terminator = terminator
        self.echo = echo
        self.command = command if command else echoline
        # the parameter is named exiter, must not conflict with built-in exit
        self.exit = exiter

    def getchar(self):
        """
        Get character from console keyboard, add to command line, or use
         control keys: http://www.unix-manuals.com/refs/misc/ascii-table.html
        RET, Enter, or ^M: Execute command line
        DEL, BS, or ^H: Remove last character from command line
        ^L, FF: Redisplay prompt and command line (useful after DELs)
        ^U, NAK: Discard command line, display new prompt
        ^D: EOT at start of line: exit Piety, return to Python prompt
        ^C: ETX: interrupt Piety, print traceback, pop out to Python prompt
        """
        c = terminal.getchar()
        # command line done, execute command
        if c == self.terminator: # cmdline does NOT include terminator
            self.do_command()
        # control keys and command line editing
        elif c in ('\b', '\x7F'): # (backspace, delete) treated the same
            last = self.cmdline[-1] if self.cmdline else ''
            self.cmdline = self.cmdline[:-1] # remove last character
            if self.echo:
                # terminal.putstr('^H') # old-timers will recognize this
                terminal.putstr('\\%s' % last) # maybe more helpful than ^H
        elif c == '\f' : # form feed, ^L, redisplay cmdline, useful after ^H
            # no change to cmdline
            terminal.putstr('^L\r\n' + self.prompt + self.cmdline) # on new line
        elif c == '\x15': # ^U discard cmdline, display prompt on new line
            self.cmdline = str() 
            terminal.putstr('^U\r\n' + self.prompt) 
        elif c == '\x04': # ^D, ascii EOT, exit Piety
            # only exit if cmdline is empty, same behavior as Python
            if not self.cmdline and self.exit:
                terminal.putstr('^D') 
                terminal.restore() 
                print # start new line
                self.exit() # call exiter
            elif not self.cmdline and not self.exit:
                terminal.putstr('^D\r\n' + noexit + '\r\n' + self.prompt)
            else: 
                pass # if cmdline is not empty, ^D does nothing, not even echo
        # raw mode terminal doesn't respond to ^C, must handle here
        elif c == '\x03' : # ^C, ascii ETX, interrupt Piety
            terminal.putstr('^C') 
            terminal.restore() # on new line...
            print              # ... otherwise traceback is a mess
            raise KeyboardInterrupt
        # end of control keys and command line editing
        # handle ordinary non-control characters:
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
        terminal.setup() # enter or resume single character mode

