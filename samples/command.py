"""
command.py - Skeleton terminal application.
  Collects a command (string), passes it to a handler (callable) to execute.
  Can collect command without blocking for cooperative multitasking.
  Provides command history, editing similar to Unix readline, Python raw_input

Has a main method, python command.py demonstrates most functions.
"""

import sys
import string # for string.printable
import terminal

# For terminals where pressing the Control key sends ASCII control codes,
#  up and down keys send ANSI control sequences.
# Replace these imports to use a different kind of keyboard or display
import vt_keyboard as keyboard
import ansi_display as display

quit = False

def echo(command):
    'Default handler, print command on console, exit after q'
    global quit
    print command
    if command == 'q':
        quit = True

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

class Command(object):
    def __init__(self, prompt='> ', handler=echo):
        """
        prompt - Prompt string that appears at the start of each line
          Default is '> '
        handler - Function to execute command
          Can be any callable that takes one argument, a string.
          Default just echoes the command.
        """
        self.command = '' # command string 
        self.point = 0  # index where next character will be inserted
        self.prompt = prompt # string to prompt for command 
        self.handler = handler # callable that executes command string
        self.history = list() # list of commands, earliest first
        self.hindex = 0 # index into history
        # prompt used for continuation lines: '...' as long as self.prompt
        self.continuation = '.'*(len(self.prompt)-1) + ' ' 

        # keymap must be an attribute because its values are bound methods
        # keys in keymap can be multicharacter sequences, not just single chars
        # update or reassign keymap to use different keys, methods
        self.keymap = {
            # This entry requires special-case handling
            #  because it takes an additional argument: the key
            # Use this with printing terminals, comment out now
            #  string.printable: self.self_append_command,
            # This requires display terminal with cursor addressing
            string.printable: self.self_insert_command,

            # these entries work on a printing terminal
            keyboard.cr: self.accept_line,
            keyboard.C_c: self.interrupt,
            keyboard.C_j: self.newline,
            keyboard.C_l: self.redraw_current_line,
            keyboard.C_u: self.line_discard,
            keyboard.C_p: self.previous_history,
            keyboard.C_n: self.next_history,

            # Rudimentary in-line editing, just delete last char in line
            # Use these with printing terminals, commented out now
            # keyboard.bs: backward_delete_last_char,
            # keyboard.delete: backward_delete_last_char,

            # editing that requires a display terminal with cursor addressing
            # must remove all these when using printing terminals
            keyboard.bs: self.backward_delete_char,
            keyboard.delete: self.backward_delete_char,
            keyboard.C_a: self.move_beginning_of_line,
            keyboard.C_b: self.backward_char,
            keyboard.C_d: self.delete_char,
            keyboard.C_e: self.move_end_of_line,
            keyboard.C_f: self.forward_char,
            keyboard.C_k: self.kill_line,

            # These keys are multicharacter control sequences
            # require keyboard that sends ANSI control sequences
            keyboard.right: self.forward_char,
            keyboard.left: self.backward_char,
            keyboard.up: self.previous_history,
            keyboard.down: self.next_history,
            }

    def handle_key(self, key):
        'Collect command string and dispatch on command'
        # key arg might be single character or a sequence of characters
        if key in string.printable[:-5]: # exclude \t\n\r\v\f at the end
            self.keymap[string.printable](key)
        elif key in self.keymap:
            self.keymap[key]() # fcn not method needs self arg
        else:
            print keyboard.bel, # sound indicates key not handled
        return key # caller might check for 'q' quit cmd or ...

    # Methods, not directly invoked by keys in keymap

    def do_command(self):
        'Process command string and restart'
        terminal.set_line_mode() # resume line mode for command output
        print # print command output on new line
        self.handler(self.command)
        self.restart() # not quite right after q command, prints prompt again

    def restart(self):
        'Clear command line, print command prompt, set single-char mode'
        self.command = str()
        self.point = 0
        terminal.putstr(self.prompt) # prompt does not end with \n
        terminal.set_char_mode()

    # All the other methods are invoked via keymap

    # Methods that work on printing terminals

    def accept_line(self):
        self.history.append(self.command) # save command in history list
        self.hindex = len(self.history)-1
        self.do_command()

    def interrupt(self):
        # raw mode terminal doesn't respond to ^C, must handle here
        terminal.putstr('^C') 
        terminal.set_line_mode() # on new line...
        print              # ... otherwise traceback is a mess
        raise KeyboardInterrupt

    # Simple command editing that works on printing terminals

    def self_append_command(self, key):
        'Append last character on line, works on printing terminals'
        self.command += key
        self.point += 1
        terminal.putstr(key)

    def backward_delete_last_char(self):
        'Delete last character on line, works on printing terminals'
        if self.point > 0:
            ch = self.command[-1]
            self.command = self.command[:-1]
            self.point -= 1
            # terminal.putstr('^H') # omit, it is more helpful to echo
            terminal.putstr('\\%s' % ch) # echo \c where c is deleted char

    def redraw_current_line(self):
        terminal.putstr('^L\r\n' + self.prompt)  # on new line
        putlines(self.command) # might be multiple lines

    def line_discard(self): # name like gnu readline unix-line-discard
        self.command = str() 
        self.point = 0
        terminal.putstr('^U\r\n' + self.prompt)

    def newline(self):
        self.command += '\n'
        self.point += 1
        terminal.putstr('^J\r\n' + self.continuation)

    # Command history, works on printing terminals

    def previous_history(self):
        if self.history:
            self.command = self.history[self.hindex]
        self.point = len(self.command)
        self.hindex = self.hindex - 1 if self.hindex > 0 else 0
        terminal.putstr('^P\r\n' + self.prompt) # on new line
        putlines(self.command) # might be multiple lines

    def next_history(self):
        self.hindex = self.hindex + 1 \
            if self.hindex < len(self.history)-1 else self.hindex
        if self.history:
            self.command = self.history[self.hindex]
        self.point = len(self.command)
        terminal.putstr('^N\r\n' + self.prompt)  # on new line
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

# Test

def main():
    global quit
    quit = False # earlier invocation might have set it True
    c = Command()
    c.restart()
    while not quit:
        # multi-char control sequences keyboard.up,down don't work here
        k = terminal.getchar()
        c.handle_key(k)
    terminal.set_line_mode()

if __name__ == '__main__':
    main()
