"""
command.py - Command class, skeleton command line application.  

Collects a command (string) one keycode at a time, passes it to a
   handler (callable) to execute.

Delegates in-line editing of the command string to another class,
a simple stub class is included in this module.

Provides command history similar to readline.

Has hooks for job control commands that can bypass or suspend
   application, other hooks for routing keycodes to other classes, for
   example to support editors with a command mode (this class) and
   insert modes (other classes).

This module has similar motivation to the Python standard library cmd
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
printing_chars = string.printable[:-5] # exclude \t\n\r\v\f at the end

# This keymap works on a printing terminal.
printing_keymap = {
    # any keycode that maps to accept_line is a command terminator
    keyboard.cr: 'accept_line',
    keyboard.C_c: 'interrupt',
    keyboard.C_p: 'previous_history',
    keyboard.C_n: 'next_history',
    }

# This keymap requires a display terminal with cursor addressing.
#  Some of the keys redefine entries in printing_keymap, above.
vt_keys = {
    keyboard.up: 'previous_history',
    keyboard.down: 'next_history',
    }

vt_keymap = printing_keymap.copy()
vt_keymap.update(vt_keys)

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


class LineInput(object):
    'Minimal placeholder for command_line object, no editing'
    def __init__(self, keymap={c: None for c in printing_chars}):
        self.chars = ''  # Command restart() reinitializes when needed
        self.keymap = keymap

    def handler(self, keycode):
        'Stub, no need to dispatch anything, just echo and append key'
        util.putstr(keycode)
        self.chars += keycode
            

class Command(object):
    def __init__(self, prompt='', reader=terminal.getchar, 
                 command_mode=(lambda: True), command_line=LineInput(),
                 do_command=(lambda command: None),  # do nothing
                 stopped=(lambda command: False),    # never exit
                 keymap=vt_keymap, job_control=job_control_keymap): # defined above
        """
        All arguments are optional, with defaults

        prompt - Prompt string that appears at the start of each line.
          Default is empty string '', no prompt.

        reader - callable to read one or more characters to build
          command string.  Takes no arguments and returns a string
          (might be just a single character).  
          Default is terminal.getchar, get a single character.

        command_mode - callable to test application mode, returns True 
          in modes where this instance should handle keycodes.
          When False, pass keycodes to a different object.
          Motivation is editors with command mode (return True)
          and insert modes (return False).
          Default is (lambda: True), always handle keycodes.

        command_line - object to collect and store command line, and
          optionally provide in-line editing.  Command line text must be
          stored in an attribute named chars, its keymap must be in
          an attribute named keymap, and there must be a method named
          dispatch that takes a keycode argument.
          Default is minimal LineInput class defined in this module.

        do_command - callable to execute command string.  Takes one
          argument, a string.  
          Default is (lambda command: None), do nothing.

        stopped - callable to test when the application should stop or
          exit.  Takes one argument, a string.  Typically this is the
          command string, so stopped() can check if command is
          something like 'exit()' or 'quit' - but stopped() might
          ignore this string and check some state variable instead.
          Default is (lambda command: False), never exit.

        keymap: dictionary from keycode to Command method name string

        job_control: dictionary from keycode to job control method name string
        """
        self.prompt = prompt # string to prompt for command 
        self.reader = reader # callable, reads char(s) to build command string
        self.command_mode = command_mode
        self.command_line = command_line
        self.command_line.chars = ''
        self.command_line.prompt = self.prompt
        self.do_command = (lambda: do_command(self.command_line.chars))
        self.stopped = (lambda: stopped(self.command_line.chars))
        self.job = None  # assign elsewhere, then here use self.job.stop() etc.
        self.history = list() # list of previous commands, earliest first
        self.hindex = 0 # index into history
        # prompt used for continuation lines: '...' same len as self.prompt
        self.continuation = '.'*(len(self.prompt)-1) + ' ' 
        self.keymap = keymap
        self.job_control = job_control

    def handler(self):
        'Read char, add to keycode sequence.  If seq complete, handle keycode'
        # to avoid blocking in self.reader(), must only call when input is ready
        keycode = self.reader() # returns '' when keycode is not yet complete
        # keycode might be single character or a sequence of characters.
        # Check job keymap before ordinary keymap, same keys can appear in both.
        # Job control commands must be a single keycode at start of line.
        if keycode and (keycode in self.job_control 
                        and self.command_line.chars == ''):
            self.command_line.chars = keycode # so job control code can find it
            method = getattr(self, self.job_control[keycode])
            method()
            # For now, all job control commands exit
            self.restore()     # calls print() for newline
            if self.job:
                self.job.do_stop() # callback to job control
            return
        elif keycode and keycode in self.keymap:
            method = getattr(self, self.keymap[keycode])
            method()
        elif keycode and (keycode in printing_chars or 
                          keycode in self.command_line.keymap):
            self.command_line.handler(keycode)
        elif keycode:
            print(keyboard.bel, end=' ') # sound indicates key not handled
        else:
            pass # incomplete keycode, do nothing

    def restart(self):
        'Clear command string, print command prompt, set single-char mode'
        self.command_line.chars = ''
        self.command_line.prompt = self.prompt # it might have changed
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
        self.history.append(self.command_line.chars) # save command in history
        self.hindex = len(self.history)-1
        self.restore()    # advance line and put terminal in line mode 
        self.do_command() # application executes command
        if self.job and self.job.replaced: # command may replace or stop app
            return
        elif self.stopped() and self.job:
            self.job.do_stop() # callback to job control
        else:
      	    self.restart()# print prompt and put term in character mode

    def interrupt(self):
        'Handle ^C, exit from Piety'
        # raw mode terminal doesn't respond to ^C, must handle here
        util.putstr('^C') 
        terminal.set_line_mode() # on new line...
        print()              # ... otherwise traceback is a mess
        raise KeyboardInterrupt

    # Command history, works on printing terminals

    def previous_history(self):
        if self.history:
            length = len(self.history)
            self.hindex = self.hindex if self.hindex < length else length-1
            self.command_line.chars = self.history[self.hindex]
        self.point = len(self.command_line.chars)
        self.hindex = self.hindex - 1 if self.hindex > 0 else 0
        util.putstr('^P\r\n' + self.prompt) # on new line
        putlines(self.command_line.chars) # might be multiple lines

    def next_history(self):
        length = len(self.history)
        self.hindex = self.hindex + 1 if self.hindex < length else length
        self.command_line.chars = (self.history[self.hindex] if self.hindex < length 
                                 else '')
        self.point = len(self.command_line.chars)
        util.putstr('^N\r\n' + self.prompt)  # on new line
        putlines(self.command_line.chars) # might be multiple lines

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
    while c.command_line.chars not in c.job_control: # use job control for exit
        # Here Command instance works in reader mode:
        # uses the function passed to its handler argument to read its input.
        c.handler()
        # Alternatively, here Command instance works in receiver mode:
        # uses its built-in dispatch method to accept input passed by caller.
        # To demonstrate, comment out previous line and uncomment following lines 
        #char = terminal.getchar()
        #c.handler(char)
    c.restore()

if __name__ == '__main__':
    # default()
    main()
