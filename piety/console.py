"""
console.py - Skeleton command line application.
  Collects a command line and passes it to a given command to execute.
  Can collect command line without blocking for cooperative multitasking.
  Provides command history, simple editing that works on printing terminals.
  Provides hook for display editing and other options.

Has a main method, python console.py demonstrates most functions.
"""

import sys
import string # for string.printable
import terminal

# For terminals where pressing the Control key sends ASCII control codes,
#  up and down keys send ANSI control sequences.
# Printing terminals will work.
# Replace this import to use a different kind of keyboard.
import vt_keyboard as keyboard

def echo(line):
    'Default command, print line on console'
    print line

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

class Console(object):

    # class variable, might be used by multiple instances
    # True when same console instance will continue after do_command
    # Usually True, but False when do_command resumes a different console task
    # Set False by __call__ below, restored True by do_command below
    continues = True # recall 'continue' (with no s) is a Python keyword

    def __init__(self, prompt='> ', command=echo, 
                 resume=None, quit=None, pause=None, 
                 optional_keymap=None): 
        """
        prompt - Prompt string that appears at the start of each line
          Default is '> '
        command - Function to execute command line
          Can be any callable that takes one argument, a string.
          Default just echoes the command line.
        resume - optional argument, function to call to initialize
          terminal before accepting input.
        quit - optional argument, function to call to exit application,
           which is called if you type ^D at an empty command line.
          Default simply prints message advising you can type ^C
        pause - optional argument, function to call to clean up
          terminal after quit is executed.  
          Default does nothing - often nothing is needed.
        optional_keymap - keymap for additional functions such as
          in-line editing, default is None.  Entries in this keymap
          override entries in basic_keymap that have the same key.
        """
        self.chars = '' # command line
        self.point = 0  # index where next character will be inserted
        self.prompt = prompt
        self.command = command
        self.resume = resume
        self.quit = quit
        self.pause = pause
        self.history = list() # list of command lines, earliest first
        self.iline = 0 # index into history
        self.continuation = '.'*(len(self.prompt)-1) + ' ' # prompt

        # Merge keymaps, entries in optional_keymap override basic_keymap
        # Copy dictionary so other clients of this module don't see updates
        self.keymap = basic_keymap.copy() # basic_keymap defined below
        self.keymap.update(optional_keymap if optional_keymap else {})

    def handle_key(self, key):
        'Collect command line and dispatch on command'
        # key arg might be single character or a sequence of characters
        # Special cases for ^D, otherwise ^D is handled by keymap
        if key == keyboard.C_d and not self.chars and not self.quit:
            terminal.putstr('^D\r\n' + noexit + '\r\n' + self.prompt)
        elif key == keyboard.C_d and  not self.chars and self.quit:
            self.end_of_file()
        elif key in self.keymap:
            self.keymap[key](self) # fcn not method needs self arg
        elif key in string.printable:
            self.keymap[string.printable](self, key)
        else:
            print keyboard.bel, # sound indicates key not handled
        return key # caller might check for 'q' quit cmd or ...

    # Methods, not directly invoked by keys in basic_keymap

    def do_command(self):
        'Process command line and restart'
        # special case for self.pause so we *don't* restart, but cleanup
        if self.chars == self.quit.__name__ : # If None, ^D is only way out
          self.do_pause()
        else:
          terminal.restore() # resume line mode for command output
          print # print command output on new line
          self.command(self.chars) # might quit, set Console.continues = False
          if Console.continues:  # typical case - self.command was not quit
              self.restart(self.prompt) # print prompt, resume single char mode
          else: # self.command was quit, set Console.continues = False
              self.chars = str() # clear these, anticipating after next pause
              self.point = 0
              Console.continues = True # keep executing new Console instance

    def restart(self, prompt):
        'Clear command line, print command prompt, set single-char mode'
        self.chars = str()
        self.point = 0
        terminal.putstr(prompt) # prompt does not end with \n
        terminal.setup() # enter or resume single character mode

    def __call__(self):
        'Configure terminal display and prepare to accept input'
        if self.resume:
          self.resume()
        self.restart(self.prompt)
        Console.continues = False # instead resume different Console instance

    def end_of_file(self):
        'Handle end-of-file key'
        terminal.putstr('^D\r\n') # we're still in terminal raw mode
        self.do_pause() # restores terminal

    def do_pause(self):
        'Clear command line, exit and cleanup, print piety prompt'
        self.chars = str()
        self.point = 0
        if self.quit:
          self.quit()
        else:
          print 'No quit function defined, type ^C for KeyboardInterrupt'
        if self.pause:
          self.pause()
        # here we actually want to restart not self but successor console
        print # prompt on new line
        self.restart('>> ') # for now, successor is always piety.

# Command functions for the basic_keymap table defined below.
# All of these commands work on printing terminals.

# The commands are *not* methods in the Console class.
# They are ordinary functions in the console module.  They take
#  the console object as the ordinary argument c, not the self argument.
# Therefore the commands defined here have the same form of argument lists
#  as the commands passed in with the optional_keys keymap.
# This enables basic_keys and optional_keys to be merged with dict update
#  and be treated uniformly in handle_key.

def accept_line(c):
    c.history.append(c.chars) # save command in history list
    c.iline = len(c.history)-1
    c.do_command()

def interrupt(c):
    # raw mode terminal doesn't respond to ^C, must handle here
    terminal.putstr('^C') 
    terminal.restore() # on new line...
    print              # ... otherwise traceback is a mess
    raise KeyboardInterrupt

# Simple command line editing that works on printing terminals

def self_append_command(c, key):
    'Append last character on line, works on printing terminals'
    c.chars += key
    c.point += 1
    terminal.putstr(key)

def backward_delete_last_char(c):
    'Delete last character on line, works on printing terminals'
    if c.point > 0:
        ch = c.chars[-1]
        c.chars = c.chars[:-1]
        c.point -= 1
        # terminal.putstr('^H') # omit, it is more helpful to echo
        terminal.putstr('\\%s' % ch) # echo \c where c is deleted char

def redraw_current_line(c):
    terminal.putstr('^L\r\n' + c.prompt)  # on new line
    putlines(c.chars) # might be multiple lines

def line_discard(c): # name like gnu readline unix-line-discard
    c.chars = str() 
    c.point = 0
    terminal.putstr('^U\r\n' + c.prompt)

def newline(c):
    c.chars += '\n'
    c.point += 1
    terminal.putstr('^J\r\n' + c.continuation)

# Command line history, works on printing terminals

def previous_history(c):
    if c.history:
        c.chars = c.history[c.iline]
    c.point = len(c.chars)
    c.iline = c.iline - 1 if c.iline > 0 else 0
    terminal.putstr('^P\r\n' + c.prompt) # on new line
    putlines(c.chars) # might be multiple lines

def next_history(c):
    c.iline = c.iline + 1 if c.iline < len(c.history)-1 else c.iline
    if c.history:
        c.chars = c.history[c.iline]
    c.point = len(c.chars)
    terminal.putstr('^N\r\n' + c.prompt)  # on new line
    putlines(c.chars) # might be multiple lines

# Keymap for basic operations, uses command functions defined above

basic_keymap = {
    keyboard.cr: accept_line,
    keyboard.C_c: interrupt,
    keyboard.C_j: newline,
    keyboard.C_l: redraw_current_line,
    keyboard.C_u: line_discard,
    keyboard.C_p: previous_history,
    keyboard.C_n: next_history,
    # next two entries require keys that send ANSI control sequences
    keyboard.up: previous_history,
    keyboard.down: next_history,
    # rudimentary in-line editing, just delete last char in line
    keyboard.bs: backward_delete_last_char,
    keyboard.delete: backward_delete_last_char,
    # this entry requires special-case handling in program logic
    string.printable: self_append_command
    }

# Test

quit = False

def q():
    global quit
    quit = True
  
def main():
    global quit
    quit = False # earlier invocation might have set it True
    c = Console(quit=q)
    c() # prompt first time, execute terminal.setup()
    while not quit:
        # multi-char control sequences like keyboard.up don't work here
        k = terminal.getchar()
        c.handle_key(k)
    # After q or ^D, c.handle_key executes c.pause with terminal.restore()

if __name__ == '__main__':
    main()
