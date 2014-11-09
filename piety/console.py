"""
console.py - skeleton command line application for Piety

Defines Console class and Command class.

The Console class has a getchar method that gets a single character
typed at the console keyboard, and adds it to a command line
(usually).  When getchar gets a line terminator character, it calls a
command function and passes the command line to it.

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

The Command class makes a console instance into a command (callable)
that can be invoked conveniently from the Piety shell.  It manages
console focus, initialization, and cleanup.
"""

import sys
import string

# These imports hide platform dependencies.
import terminal
# For vt100-style terminal with ansi escape sequences, arrow keys.
# Replace these two imports to use a different keyboard and display.
import vt_keyboard as keyboard
import vt_display as display

# Print regrets when ^D but no self.exit
noexit = 'No exit function defined, type ^C for KeyboardInterrupt'

# focus is the Console task that has console focus:
# the task whose command function is called when command line is complete
focus = None

def change_focus(new_focus):
  'change console focus to console instance new_focus'
  global focus
  focus = new_focus

def putlines(s):
    """
    Format and print possibly multi-line string
    at each linebreak print \r\n
    """
    lines = s.splitlines()
    lastline = len(lines) - 1 # index of last line
    for iline, line in enumerate(lines):
        terminal.putstr(line)
        if iline < lastline:
            terminal.putstr('\r\n')

def echoline(cmdline):
    'Print cmdline on console'
    print cmdline

class Console(object):
    """
    Skeleton command line application for Piety.  Has a getchar method
    that gets a key typed at the console and adds it to a command
    line (usually).  

    Schedule getchar from the Piety scheduler for non-blocking command
    input.  When getchar gets a line terminator character, it calls a
    command function and passes the command line to it.  

    The 'key' might actually be a multi-character control sequence (as
    in Emacs).  Some of the keys do command line editing.
    """
    def __init__(self, prompt='> ', command=None, exiter=exit):
        """
        prompt - optional argument, prompt string, default is 'piety>'
        command - optional argument, function to execute command line,
          can be any callable that takes one argument, a string.
          Default just echoes the command line.
        exiter - optional argument, function to call in response to ^D key.
          default merely prints a line advising ^C to interrupt.
        """
        self.cmdline = str()
        self.point = 0 # index where next character will be inserted
        self.prompt = prompt
        self.command = command if command else echoline # fcn to call
        # the parameter is named exiter to avoid clash with built-in exit
        # self.exit is okay because it is not ambiguous
        self.exit = exiter # function to call to exit
        self.history = list() # list of cmdline, earliest first
        self.iline = 0 # index into cmdline history
        self.continuation = '.'*(len(self.prompt)-1) + ' ' # prompt

        # associate keys with commands (methods)
        # edit here or reassign later to change key assignments
        # command names are from emacs or gnu readline 
        self.keymap = { 
            # command line management
            keyboard.cr: self.accept_line,
            keyboard.C_l: self.redraw_current_line,
            keyboard.C_u: self.line_discard,
            keyboard.C_j: self.newline,
            keyboard.C_p: self.previous_history,
            keyboard.up: self.previous_history,
            keyboard.C_n: self.next_history,
            keyboard.down: self.next_history,
            keyboard.C_c: self.interrupt,
            # line editing
            keyboard.bs: self.backward_delete_char,
            keyboard.delete: self.backward_delete_char,
            keyboard.C_a: self.move_beginning_of_line,
            keyboard.C_b: self.backward_char,
            keyboard.left: self.backward_char,
            keyboard.C_e: self.move_end_of_line,
            keyboard.C_f: self.forward_char,
            keyboard.right: self.forward_char,
            keyboard.C_k: self.kill_line,
            # keys used in both modes
            keyboard.C_d: self.handle_C_d,
            # printable characters: self.self_insert_command, below
            }

    # Command line management
    # These functions all start a new command line, never edit in line,
    # so they all work on printing terminals.

    def accept_line(self):
        self.history.append(self.cmdline) # save command in history list
        self.iline = len(self.history)-1
        self.do_command()

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
        # not self.prompt, the cmd fcn may have changed the focus # FIXME?
        terminal.putstr(focus.prompt) # prompt does not end with \n
        terminal.setup() # enter or resume single character mode

    def redraw_current_line(self):
        terminal.putstr('^L\r\n' + self.prompt)  # on new line
        putlines(self.cmdline) # might be multiple lines

    def newline(self):
        self.cmdline += '\n'
        self.point += 1
        terminal.putstr('^J\r\n' + self.continuation)

    def previous_history(self):
        if self.history:
            self.cmdline = self.history[self.iline]
        self.point = len(self.cmdline)
        self.iline = self.iline - 1 if self.iline > 0 else 0
        terminal.putstr('^P\r\n' + self.prompt) # on new line
        putlines(self.cmdline) # might be multiple lines

    def next_history(self):
        self.iline = self.iline + 1 \
            if self.iline < len(self.history)-1 else self.iline
        if self.history:
            self.cmdline = self.history[self.iline]
        self.point = len(self.cmdline)
        terminal.putstr('^N\r\n' + self.prompt)  # on new line
        putlines(self.cmdline) # might be multiple lines

    def line_discard(self): # name like gnu readline unix-line-discard
        self.cmdline = str() 
        self.point = 0
        terminal.putstr('^U\r\n' + self.prompt)

    def interrupt(self):
        # raw mode terminal doesn't respond to ^C, must handle here
        terminal.putstr('^C') 
        terminal.restore() # on new line...
        print              # ... otherwise traceback is a mess
        raise KeyboardInterrupt

    def handle_C_d(self):
        # two modes: manage command line or edit in line
        if not self.cmdline and not self.exit:
            terminal.putstr('^D\r\n' + noexit + '\r\n' + self.prompt)
        elif not self.cmdline and self.exit:
            self.end_of_file()
        else: # edit in line
            self.delete_char() # with line editing, below

    def end_of_file(self):
        terminal.putstr('^D') 
        terminal.restore() 
        print # start new line
        self.point = 0
        self.exit() # call exiter

    # Line editing
    # None of these functions start a new line, they edit line in place.
    # They accommodate a leading prompt, if one is present.

    # The following work on printing terminals
    # (they are not included in the keymap above)

    def self_append_command(self, key):
        'Append last character on line, works on printing terminals'
        self.cmdline += key
        self.point += 1
        terminal.putstr(key)

    def backward_delete_last_char(self):
        'Delete last character on line, works on printing terminals'
        if self.point > 0:
            ch = self.cmdline[-1]
            self.cmdline = self.cmdline[:-1]
            self.point -= 1
            # terminal.putstr('^H') # omit, it is more helpful to echo
            terminal.putstr('\\%s' % ch) # echo \ + deleted character

    # The following all require video terminals with cursor addressing;
    #  they do not work on printing terminals.
    # They all appear in the keymap above.

    def self_insert_command(self, key):
        self.cmdline = (self.cmdline[:self.point] 
                        + key + self.cmdline[self.point:])
        self.point += 1
        display.self_insert_char(key)

    def backward_delete_char(self):
        if self.point > 0:
            self.cmdline = (self.cmdline[:self.point-1] 
                            + self.cmdline[self.point:])
            self.point -= 1
            display.backward_delete_char()

    def move_beginning_of_line(self):
        self.point = 0
        start = len(self.prompt)+1 # allow for space after prompt
        display.move_to_column(start) # move to character after prompt

    def backward_char(self):
        if self.point > 0:
            self.point -= 1
            display.backward_char()

    def delete_char(self):
        self.cmdline = (self.cmdline[:self.point] 
                        + self.cmdline[self.point+1:])
        display.delete_char()

    def move_end_of_line(self):
        self.point = len(self.cmdline)
        eol = len(self.prompt) + 1 + len(self.cmdline)
        display.move_to_column(eol)

    def forward_char(self):
        if self.point < len(self.cmdline):
            self.point += 1
            display.forward_char()

    def kill_line(self):
         self.cmdline = self.cmdline[:self.point] # point doesn't change
         display.kill_line()

    # getchar function

    # FIXME We would like to rename getchar to getkey,
    # but then we would have to change several scripts that use it.
    def getchar(self):
        """
        Get key from console keyboard.
        The key may be a multi-character control sequence (as in Emacs)
        Then execute the command for that key
        """
        key = terminal.getchar()
        
        # Collect entire ansi control sequence within a single call to getchar.
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

        # collect escape sequence here - otherwise key is single char
        if key == keyboard.esc:
            c1 = terminal.getchar()
            if c1 != '[':
                return # discard esc c1, not ansi ctl seq introducer (csi).
            else:
                key += c1
                c2 = terminal.getchar()
                if c2 not in 'ABCD':  # four arrow keys are esc[A etc.
                    return # discard esc [ c2, not one of the 4 arrow keys
                else:
                    key += c2 
                    # print ('key: %s' % [c for c in key]) # DEBUG
                    # arrow key detected, one of ansi.cuf1 etc.

        if key in self.keymap:
            self.keymap[key]()
        elif key in string.printable:
            self.self_insert_command(key)
        else:
            print keyboard.bel, # sound indicates key not handled


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
