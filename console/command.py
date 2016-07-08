"""
command.py - Skeleton command line application.  Collects a
  command (string), passes it to a handler (callable) to execute.  Can
  collect a command one character at a time without blocking to permit
  cooperative multitasking (unlike Python *input*, which blocks until
  the command is complete).  Provides command history and editing
  similar to Unix *readline* (but no tab completion).  Provides hooks
  for optional job control commands that bypass the application.

This module has a main method, so python command.py demonstrates some
functions.

A Command instance can work in reader mode where it uses the
function passed to the handler initializer argument to read input,
or, alternatively, can work in receiver mode where it uses
the built-in handle_key method to accept input passed from a caller.
This module's main function demonstrates both alternatives.

This module has some similarities to the Python standard library cmd
module, but does not provide the same API.
"""

import sys
import string # for string.printable
import util, terminal, keyboard, display

# A keymap is a dictionary from keycode string to Command method name string.
# Values are name strings not function objects, so they can refer to bound methods.
# Keycodes in keymap can be multicharacter sequences, not just single characters.
# Most method names in the keymap are the same as in GNU readline or Emacs.

# FIXME first define printing_keymap, then update it to create editing_keymap.

# This editing_keymap requires a display terminal with cursor addressing.
editing_keymap = {
    # self_insert_command requires special-case handling
    #  because it takes an additional argument: the key.
    # Use this function with printing terminals, comment out now:
    #  string.printable: 'self_append_command',
    # This function requires display terminal with cursor addressing:
    string.printable: 'self_insert_command',

    # these entries work on a printing terminal
    keyboard.cr: 'accept_line',
    keyboard.C_c: 'interrupt',
    keyboard.C_j: 'newline',
    keyboard.C_l: 'redraw_current_line',
    keyboard.C_u: 'line_discard',
    keyboard.C_p: 'previous_history',
    keyboard.C_n: 'next_history',

    # Rudimentary in-line editing, just delete last char in line
    # Use these with printing terminals, commented out now
    # keyboard.bs: backward_delete_last_char',
    # keyboard.delete: backward_delete_last_char',

    # editing that requires a display terminal with cursor addressing
    # must remove all these when using printing terminals
    keyboard.bs: 'backward_delete_char',
    keyboard.delete: 'backward_delete_char',
    keyboard.C_a: 'move_beginning_of_line',
    keyboard.C_b: 'backward_char',
    keyboard.C_d: 'handle_C_d', # exit or 'delete_char
    # keyboard.C_d: 'delete_char
    keyboard.C_e: 'move_end_of_line',
    keyboard.C_f: 'forward_char',
    keyboard.C_k: 'kill_line',

    # These keys are multicharacter control sequences
    # require keyboard that sends ANSI control sequences
    keyboard.right: 'forward_char',
    keyboard.left: 'backward_char',
    keyboard.up: 'previous_history',
    keyboard.down: 'next_history',
    }

# used by Command to print history to print current 'line' including newlines
def putlines(s):
    """
    Format and print possibly multi-line string
    at each linebreak print \r\n
    """
    lines = s.splitlines()
    lastline = len(lines) - 1 # index of last line
    for iline, line in enumerate(lines):
        util.putstr(line)
        if iline < lastline:
            util.putstr('\r\n')

class Command(object):
    def __init__(self, prompt='', handler=terminal.getchar, 
                 do_command=(lambda command: None),  # do nothing
                 stopped=(lambda command: False),    # never exit
                 keymap=editing_keymap):             # defined above
        """
        All arguments are optional, with defaults
s
        prompt - Prompt string that appears at the start of each line.
        Default is empty string '', no prompt.

        handler - callable to read one or more characters
        to build command string.  Takes no arguments and returns a
        string (might be just a single character).  Default is
        terminal.getchar.

        do_command - callable to execute command string.  Takes one
        argument, a string.  Default does nothing.

        stopped - callable to test command string, that returns True
        when the application should stop or exit.  Takes one argument,
        a string.  Typically this is the command string, stopped() can
        check if command is something like 'exit()' or 'quit' - but
        stopped() might ignore this string and check some state
        variable.  Default always returns False - never exit (caller
        could still force exit).

        keymap: dictionary from keycode to Command method name string
        """
        self.prompt = prompt # string to prompt for command 
        self.handler_body = handler # callable reads char(s) to build command string
        self.do_command = (lambda: do_command(self.command))
        self.stopped = (lambda: stopped(self.command))
        self.job = None  # can assign console.job = job then use console.job.replaced
        self.job_commands = [ keyboard.C_d ] # ^D exit, job cmds bypass application
        self.command = '' # command string 
        self.point = 0  # index of insertion point in self.command
        self.history = list() # list of previous commands, earliest first
        self.hindex = 0 # index into history
        # prompt used for continuation lines: '...' same len as self.prompt
        self.continuation = '.'*(len(self.prompt)-1) + ' ' 
        self.keymap = keymap

    def handle_key(self, keycode):
        'Collect command string and dispatch on command'
        # keycode arg might be single character or a sequence of characters.
        # Printable keys require special-case handling,
        # because their method takes an additional argument: the key.
        if keycode in string.printable[:-5]: # exclude \t\n\r\v\f at the end
            method = getattr(self, self.keymap[string.printable])
            method(keycode)
        elif keycode in self.keymap:
            method = getattr(self, self.keymap[keycode])
            method()
        else:
            print(keyboard.bel, end=' ') # sound indicates key not handled

    def handler(self):
        'Read char, add to keycode sequence.  If sequence is complete, handle keycode'
        # might block here in self.handler_body()
        # to avoid blocking, must only call when input is ready for handler_body
        keycode = self.handler_body() 
        if keycode:
            self.handle_key(keycode)

    def restart(self):
        'Clear command string, print command prompt, set single-char mode'
        self.command = str()
        self.point = 0
        util.putstr(self.prompt) # prompt does not end with \n
        terminal.set_char_mode()

    def restore(self):
        'Restore terminal line mode, prepare to print on new line'
        terminal.set_line_mode()
        print()

    # All the other methods are invoked via keymap

    # Methods that work on printing terminals

    def accept_line(self):
        self.history.append(self.command) # save command in history list
        self.hindex = len(self.history)-1
        self.restore()        # advance line and put term in line mode 
        if self.command not in self.job_commands: # job cmds bypass application
            self.do_command() # application executes command
        if self.job and self.job.replaced: # command may replace or stop application
            return
        elif self.stopped() and self.job:
            self.job.do_stop()    # callback to job control
        else:
      	    self.restart()    # print prompt and put term in character mode

    def interrupt(self):
        # raw mode terminal doesn't respond to ^C, must handle here
        util.putstr('^C') 
        terminal.set_line_mode() # on new line...
        print()              # ... otherwise traceback is a mess
        raise KeyboardInterrupt

    # Simple command editing that works on printing terminals

    def self_append_command(self, key):
        'Append last character on line, works on printing terminals'
        self.command += key
        self.point += 1
        util.putstr(key)

    def backward_delete_last_char(self):
        'Delete last character on line, works on printing terminals'
        if self.point > 0:
            ch = self.command[-1]
            self.command = self.command[:-1]
            self.point -= 1
            # util.putstr('^H') # omit, it is more helpful to echo
            util.putstr('\\%s' % ch) # echo \c where c is deleted char

    def redraw_current_line(self):
        util.putstr('^L\r\n' + self.prompt)  # on new line
        putlines(self.command) # might be multiple lines

    def line_discard(self): # name like gnu readline unix-line-discard
        self.command = str() 
        self.point = 0
        util.putstr('^U\r\n' + self.prompt)

    def newline(self):
        self.command += '\n'
        self.point += 1
        util.putstr('^J\r\n' + self.continuation)

    # Command history, works on printing terminals

    def previous_history(self):
        if self.history:
            length = len(self.history)
            self.hindex = self.hindex if self.hindex < length else length-1
            self.command = self.history[self.hindex]
        self.point = len(self.command)
        self.hindex = self.hindex - 1 if self.hindex > 0 else 0
        util.putstr('^P\r\n' + self.prompt) # on new line
        putlines(self.command) # might be multiple lines

    def next_history(self):
        length = len(self.history)
        self.hindex = self.hindex + 1 if self.hindex < length else length
        self.command = self.history[self.hindex] if self.hindex < length else ''
        self.point = len(self.command)
        util.putstr('^N\r\n' + self.prompt)  # on new line
        putlines(self.command) # might be multiple lines

    # Command editing that requires a display terminal with cursor addressing
 
    def self_insert_command(self, key):
        self.command = (self.command[:self.point] + key + \
                        self.command[self.point:])
        self.point += 1
        display.self_insert_char(key)

    def backward_delete_char(self):
        if self.point > 0:
            self.command = (self.command[:self.point-1] + self.command[self.point:])
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

    def handle_C_d(self):
        '^D: stop if command string is empty, otherwise delete character.'
        if not self.command:
            self.command = keyboard.C_d # so self.stopped() can find it
            util.putstr('^D')  # no newline because ...
            self.restore()     # ... calls print() for newline
            if self.job:
                self.job.do_stop()     # callback to job control
        else:
            self.delete_char() # requires display terminal

    def delete_char(self):
        self.command = (self.command[:self.point] + self.command[self.point+1:])
        display.delete_char()

    def move_end_of_line(self):
        self.point = len(self.command)
        eol = len(self.prompt) + 1 + len(self.command)
        display.move_to_column(eol)

    def forward_char(self):
        if self.point < len(self.command):
            self.point += 1
            display.forward_char()

    def kill_line(self):
         self.command = self.command[:self.point] # point doesn't change
         display.kill_line()

# Test

# Default do_command, stopped: do nothing, exit immediately
c0 = Command(prompt='> ') # prompt to show restart() ran.

# echo input lines, exit at q or ^D
c = Command(prompt='> ', do_command=(lambda command: print(command)),
            stopped=(lambda command: command == 'q' or command == keyboard.C_d))

def default():
    "Collect command lines but do nothing until command 'q' exits."
    c0.restart()
    while not c0.command == 'q': # c0.stopped() is always False
        c0.handler() # does nothing 
    c0.restore() # undo restart, restore terminal line mode
    
def main():
    # Note - default handler terminal.getchar can't handle multi-char control seqs
    #  like keyboard.up, down, right, left - use ^P ^N ^F ^B instead
    c.restart()
    while not c.stopped():
        # Here Command instance works in reader mode:
        # uses the function passed to its handler argument to read its input.
        c.handler()
        # Alternatively, here Command instance works in receiver mode:
        # uses its built-in handle_key method to accept input passed by caller.
        # To demonstrate, comment out previous line and uncomment following lines 
        #char = terminal.getchar()
        #c.handle_key(char)
    c.restore()

if __name__ == '__main__':
    # default()
    main()
