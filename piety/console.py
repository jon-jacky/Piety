"""
console.py - skeleton command line application for Piety

Defines Console class and Command class.

Console has a getchar method that gets a single character typed at the
console keyboard, and adds it to a command line (usually).  When
getchar gets a line terminator character, it calls a command function
and passes the command line to it.

Getchar also provides some line editing functions and command history
(see getchar docstring).

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
so they can be different for each console instance.  It should be
possible to make different Console subclasses with different getchar
methods that provide different echo and edit behavior.

Command makes a console instance into a command (callable) that can be
invoked conveniently from the Piety shell.  It manages console focus,
initialization, and cleanup.
"""

import sys
import terminal
import ascii, ansi

def echoline(cmdline):
    'Print cmdline on console'
    print cmdline

def putlines(s):
    'Format and print possibly multi-line string, at each linebreak print \r\n'
    lines = s.splitlines()
    lastline = len(lines) - 1 # index of last line
    for iline, line in enumerate(lines):
        terminal.putstr(line)
        if iline < lastline:
            terminal.putstr('\r\n')

# Print regrets when ^D but no self.exit
noexit = 'No exit function defined, type ^C for KeyboardInterrupt'

# focus is the Console task that has console focus:
# the task whose command function is called when the command line is complete

focus = None

def change_focus(new_focus):
  'change console focus to console instance new_focus'
  global focus
  focus = new_focus

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
                 command=None, exiter=None, edit='ansi'):
        """
        prompt - optional argument, prompt string, default is 'piety>'
        terminator - optional argument, default is RETURN '\r'
        echo - optional argument, default is True
        command - optional argument, function to execute command line
          can be any callable that takes one argument, a string
          default just echoes the command line
        exiter - optional argument, function to execute in response to ^D key.
          default merely prints a line advising ^C to interrupt.
        edit - default 'ansi' for ansi cursor positioning and in-line editing
               use 'plain' for no cursor positioning, like a printing terminal
        """
        self.cmdline = str()
        self.point = 0 # index where next character will be inserted
        self.prompt = prompt
        self.terminator = terminator
        self.echo = echo
        self.command = command if command else echoline
        # the parameter is named exiter, must not conflict with built-in exit
        self.exit = exiter
        self.history = list() # list of cmdline, earliest first
        self.iline = 0 # index into cmdline history
        self.continuation = '.'*(len(self.prompt)-1) + ' ' # continuation prompt
        self.edit = edit

    def getchar(self):
        """
        Get character from console keyboard and add to command line, 
         or edit command line or access command history using control keys
        These commands work when edit='plain' or edit='ansi', 
         they do not reposition the cursor, would work on a printing terminal,
         can only add or delete characters at the end of the line:

        RET, Enter, or ^M: Execute command line
        DEL, Backspace, or ^H: Delete character before cursor
        ^J: Start new line without executing command, for multiline input
        ^L: Redisplay prompt and command line (useful after edits)
        ^U: Discard command line, display new prompt
        ^P: Retrieve previous command line from history, for edit or execution
        ^N: Retrieve next command line from history
        ^D: (empty line only) exit Piety, return to Python prompt
        ^C: (while Piety command running) interrupt command, return to Piety prompt
        ^C: (at Piety command prompt) interrupt Piety, return to Python prompt

        These additional commands reposition the cursor, work when edit='ansi',
         so you can add or delete characters anywhere in the line:
 
        ^A, left arrow: Move cursor to start of line
        ^B, right arrow: Move cursor back one character
        ^D: Delete character under cursor (non-empty line only) 
        ^E: Move cursor to end of line
        ^F: Move cursor forward one character 
        ^K: Delete from cursor to end of line
         up arrow: retrieve previous line from command history
         down arrow: retrieve next line from history
        """
        c = terminal.getchar()

        # Collect entire ansi escape sequence within a single call to getchar.
        # BECAUSE select wakes up (puts stdin in inputready) after each esc
        #  BUT remaining chars in sequence accumulate without waking up select
        #  next esc char wakes up select, then the tail of prev esc seq is read
        #  so must loop to read whole esc sequence here in a single call
        # FOR NOW just detect the four arrow keys with codes esc[A etc,
        #  must return immediately as soon as we detect esc seq is *not* arrow.
        # This code expects the *only* esc sequences will be the 4 arrow keys.
        # WARNING: This blocks waiting for at least one character after esc.
        #  Any character other than [ following esc is discarded.
        #  Any character not in ABCD following esc[ is discarded.
        # This technique can *not* be used to collect emacs-style M-x sequences
        #  typed by hand, because code blocks after M (esc) until x.
        # FIXME investigate using termios module to configure read with timeout
        #  See http://man7.org/linux/man-pages/man3/termios.3.html
        #  also http://hg.python.org/cpython/file/1dc925ee441a/Modules/termios.c
        #   regarding ICANON, c_cc[VMIN], c_cc[VTIME]
        ctlseq = '' # local variable, 
        if c == ascii.esc:
            ctlseq = c
            c1 = terminal.getchar()
            if c1 != '[':
                return # discard esc c1, not ansi ctl seq introducer (csi).
            else:
                ctlseq += c1
                c2 = terminal.getchar()
                if c2 not in 'ABCD':  # four arrow keys are esc[A etc.
                    return # discard esc [ c2, not one of the four arrow keys
                else:
                    ctlseq += c2 
                    # print ('ctlseq: %s' % [c for c in ctlseq]) # DEBUG
                    # arrow key detected, one of ansi.cuf1 etc., handle below

        # command line done, execute command
        if c == self.terminator: # cmdline does NOT include terminator
            self.history.append(self.cmdline) # save command in history list
            self.iline = len(self.history)-1
            self.do_command()

        # control keys and command line editing
        elif (c == ascii.cb or ctlseq==ansi.cub1) and self.edit == 'ansi': # ^B, back
            if self.point > 0:
                self.point -= 1
                terminal.putstr(ansi.cub % 1)
        elif (c == ascii.cf or ctlseq==ansi.cuf1) and self.edit == 'ansi': # ^F, forward
            if self.point < len(self.cmdline):
                self.point += 1
                terminal.putstr(ansi.cuf % 1)
        elif c == ascii.ca and self.edit == 'ansi':  # ^A, start of line
            self.point = 0
            start = len(self.prompt)+1 # allow for space after prompt
            terminal.putstr(ansi.cha % start)
        elif c == ascii.ce and self.edit == 'ansi':  # ^E, end of line
            self.point = len(self.cmdline)
            eol = len(self.prompt)+1+len(self.cmdline)
            terminal.putstr(ansi.cha % eol)
        elif c in ('\b', ascii.delete): # (backspace, delete) treated the same
            # delete the character *before* the cursor
            if self.point > 0:
                ch = self.cmdline[self.point-1] # so we can print it below
                self.cmdline = (self.cmdline[:self.point-1] + 
                                self.cmdline[self.point:])
                self.point -= 1
                if self.echo:
                    if self.edit == 'ansi':
                        terminal.putstr(ansi.cub % 1)
                        terminal.putstr(ansi.dch % 1)
                    else: # edit plain
                        # terminal.putstr('^H') # old-timers will recognize this
                        terminal.putstr('\\%s' % ch) # more helpful than just ^H
        elif c == '\v' and self.edit == 'ansi': # \v, ^K, delete to end of line
            self.cmdline = self.cmdline[:self.point]
            # self.point does not change
            terminal.putstr(ansi.el % 0) # 0 erases to end of line
        elif c == '\f' : # form feed, ^L, redisplay cmdline, useful after ^H
            # no change to cmdline or point
            terminal.putstr('^L\r\n' + self.prompt)  # on new line
            putlines(self.cmdline) # might be multiple lines
        elif c == ascii.cu: # ^U discard cmdline, display prompt on new line
            self.cmdline = str() 
            self.point = 0
            terminal.putstr('^U\r\n' + self.prompt) 
        elif c == '\n': # ^J linefeed, insert \n, continuatn prompt on new line
            self.cmdline += c
            terminal.putstr('^J\r\n' + self.continuation)
        elif (c == ascii.cp or ctlseq==ansi.cuu1) : # ^P prev line in history
            if self.history:
                self.cmdline = self.history[self.iline]
            self.point = len(self.cmdline)
            self.iline = self.iline - 1 if self.iline > 0 else 0
            terminal.putstr('^P\r\n' + self.prompt) # on new line
            putlines(self.cmdline) # might be multiple lines
        elif (c == ascii.cn or ctlseq==ansi.cud1): # ^N next line in history
            self.iline = self.iline + 1 \
                if self.iline < len(self.history)-1 else self.iline
            if self.history:
                self.cmdline = self.history[self.iline]
            self.point = len(self.cmdline)
            terminal.putstr('^N\r\n' + self.prompt)  # on new line
            putlines(self.cmdline) # might be multiple lines
        elif c == ascii.cd: # ^D, delete under cursor OR exit console applction
            # delete under cursor if command line is not empty
            if self.cmdline: 
                self.cmdline = (self.cmdline[:self.point] + 
                                self.cmdline[self.point+1:])
                # self.point does not change
                if self.echo and self.edit == 'ansi':
                        terminal.putstr(ansi.dch % 1)
            # only exit if cmdline is empty, same behavior as Python
            if not self.cmdline and self.exit:
                terminal.putstr('^D') 
                terminal.restore() 
                print # start new line
                self.point = 0
                self.exit() # call exiter
            elif not self.cmdline and not self.exit:
                terminal.putstr('^D\r\n' + noexit + '\r\n' + self.prompt)
            else: 
                pass # if cmdline is not empty, ^D does nothing, not even echo
        # raw mode terminal doesn't respond to ^C, must handle here
        elif c == ascii.cc: # ^C interrupt console application
            terminal.putstr('^C') 
            terminal.restore() # on new line...
            print              # ... otherwise traceback is a mess
            raise KeyboardInterrupt
        # end of control keys and command line editing

        # handle ordinary printing characters:
        else:
            self.cmdline = (self.cmdline[:self.point] + c +
                            self.cmdline[self.point:])
            self.point += 1
            if self.echo:
                if self.edit == 'ansi': # open space to insert character
                    terminal.putstr(ansi.ich % 1)
                terminal.putstr(c) # no RETURN - all c go on same line

    def do_command(self):
        'Process command line and restart'
        terminal.restore() # resume line mode for command output
        print # print command output on new line
        self.command(self.cmdline)
        self.restart()

    def restart(self):
        'Clear command line, print command prompt, set single-char mode'
        self.cmdline = str()
        self.point = 0
        # not self.prompt, the command function may have changed the focus # FIXME?
        terminal.putstr(focus.prompt) # prompt does not end with \n
        terminal.setup() # enter or resume single character mode

class Command(object):
    'Callable command object that can be invoked from the Piety shell'
    
    def __init__(self, console, run, quit, cleanup, successor):
        """
        console - console instance to be invoked by command object
        run - method to call to initialize console when command runs or resumes
        quit - method command calls to quit, we'll monkeypatch this
        cleanup - method to call to clean up console when command exits or suspends
        successor - console instance that gets focus when command exits or suspends
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


