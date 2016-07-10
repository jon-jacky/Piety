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

A Command instance can work in reader mode where it uses the function
passed to Command __init__ argument named reader to read input, or,
alternatively, can work in receiver mode where it uses the built-in
handle_key method to accept input passed from a caller.  This module's
main function demonstrates both alternatives.

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

printable = 'a' # proxy in keymaps for all printable characters

# This keymap works on a printing terminal.
printing_keymap = {
    # self_insert_command requires special-case handling
    #  because it takes an additional argument: the key.
    printable: 'self_append_command',

    # any keycode that maps to accept_line is a command terminator
    keyboard.cr: 'accept_line',
    keyboard.C_c: 'interrupt',
    keyboard.C_j: 'newline',
    keyboard.C_l: 'redraw_current_line',
    keyboard.C_u: 'line_discard',
    keyboard.C_p: 'previous_history',
    keyboard.C_n: 'next_history',

    # Rudimentary in-line editing, just delete last char in line
    keyboard.bs: 'backward_delete_last_char',
    keyboard.delete: 'backward_delete_last_char'
    }

# This keymap requires a display terminal with cursor addressing.
#  Some of the keys redefine entries in printing_keymap, above.
editing_keys = {
    printable: 'self_insert_command',

    keyboard.bs: 'backward_delete_char',
    keyboard.delete: 'backward_delete_char',
    keyboard.C_a: 'move_beginning_of_line',
    keyboard.C_b: 'backward_char',
    keyboard.C_d: 'delete_char',
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

editing_keymap = printing_keymap.copy()
editing_keymap.update(editing_keys)

# For now, job control commands must be single keycodes at start of line.
# Job keymap is checked before ordinary keymap so same keys can appear in both.
job_control_keymap = {
    keyboard.C_d: 'ctrl_d',
    keyboard.C_z: 'ctrl_z'
}

# used by Command to print history to print current 'line' including newlines
def putlines(s):
    'Format and print possibly multi-line string, at each linebreak print \r\n'
    lines = s.splitlines()
    lastline = len(lines) - 1 # index of last line
    for iline, line in enumerate(lines):
        util.putstr(line)
        if iline < lastline:
            util.putstr('\r\n')

class Command(object):
    def __init__(self, prompt='', reader=terminal.getchar, 
                 do_command=(lambda command: None),  # do nothing
                 stopped=(lambda command: False),    # never exit
                 keymap=editing_keymap, job_control=job_control_keymap): # defined above
        """
        All arguments are optional, with defaults
s
        prompt - Prompt string that appears at the start of each line.
        Default is empty string '', no prompt.

        reader - callable to read one or more characters
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

        job_control: dictionary from keycode to job control method name string
        """
        self.prompt = prompt # string to prompt for command 
        self.reader = reader # callable, reads char(s) to build command string
        self.do_command = (lambda: do_command(self.command))
        self.stopped = (lambda: stopped(self.command))
        self.job = None  # can assign console.job = job then use console.job.replaced
        self.command = '' # command string 
        self.point = 0  # index of insertion point in self.command
        self.history = list() # list of previous commands, earliest first
        self.hindex = 0 # index into history
        # prompt used for continuation lines: '...' same len as self.prompt
        self.continuation = '.'*(len(self.prompt)-1) + ' ' 
        self.keymap = keymap
        self.job_control = job_control

    def handle_key(self, keycode):
        'Collect command string and dispatch on command'
        # keycode arg might be single character or a sequence of characters.
        # For now, job control commands must be a single keycode at start of line.
        # Job keymap is checked before ordinary keymap so same keys can appear in both.
        if keycode in self.job_control and not self.command:
            self.command = keycode # so job control code can use it
            method = getattr(self, self.job_control[keycode])
            method()
            # For now, all job control commands exit
            self.restore()     # calls print() for newline
            if self.job:
                self.job.do_stop()     # callback to job control
            return
        # Printable keys require special-case handling,
        # because their method takes an additional argument: the key.
        if keycode in string.printable[:-5]: # exclude \t\n\r\v\f at the end
            method = getattr(self, self.keymap[printable])
            method(keycode)
        elif keycode in self.keymap:
            method = getattr(self, self.keymap[keycode])
            method()
        else:
            print(keyboard.bel, end=' ') # sound indicates key not handled

    def handler(self):
        'Read char, add to keycode sequence.  If sequence is complete, handle keycode'
        # to avoid blocking in self.reader(), must only call when input is ready
        keycode = self.reader() # returns '' when keycode is not yet complete
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

    # Job control commands invoked via job_control
    # Two for now just to show we can distinguish commands

    def ctrl_d(self):
        util.putstr('^D')  # no newline, caller handles it.

    def ctrl_z(self):
        print('^Z')
        util.putstr('\rStopped') # still in raw mode, print didn't RET

    # Application commands invoked via keymap

    # any keycode that maps to accept_line is a command terminator
    def accept_line(self):
        'Terminate command line, do command, possibly exit job'
        self.history.append(self.command) # save command in history list
        self.hindex = len(self.history)-1
        self.restore()        # advance line and put term in line mode 
        self.do_command() # application executes command
        if self.job and self.job.replaced: # command may replace or stop application
            return
        elif self.stopped() and self.job:
            self.job.do_stop()    # callback to job control
        else:
      	    self.restart()    # print prompt and put term in character mode

    def interrupt(self):
        'Handle ^C, exit from Piety'
        # raw mode terminal doesn't respond to ^C, must handle here
        util.putstr('^C') 
        terminal.set_line_mode() # on new line...
        print()              # ... otherwise traceback is a mess
        raise KeyboardInterrupt

    # Simple command editing that works on printing terminals

    def self_append_command(self, key):
        self.command += key
        self.point += 1
        util.putstr(key)

    def backward_delete_last_char(self):
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

# Tests - no stopped arg, but exit at any job control command: ^D ^Z

# Default do_command - echo input chars, but do nothing else
c0 = Command(prompt='> ') # prompt to show restart() ran.

# echo completed input lines
c = Command(prompt='> ', do_command=(lambda command: print(command)))

def default():
    "Collect command lines but do nothing until ^D or ^Z exits"
    c0.restart()
    while c0.command not in c0.job_control: # use job control for exit
        c0.handler() # does nothing 
    c0.restore() # undo restart, restore terminal line mode
    
def main():
    # Note - default handler terminal.getchar can't handle multi-char control seqs
    #  like keyboard.up, down, right, left - use ^P ^N ^F ^B instead
    c.restart()
    while c.command not in c.job_control: # use job control for exit
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
