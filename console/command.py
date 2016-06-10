"""
command.py - Skeleton command line application.
  Collects a command (string), passes it to do_command (callable) to execute.
  Can collect command without blocking, for cooperative multitasking.
  Provides command history, simple in-line editing similar to Unix readline.
  Provides optional hooks for job control commands that bypass the application.
 Has a main method, so python command.py demonstrates most functions.

A Command instance can work in reader mode where it uses the
function passed to the handler initializer argument to read input,
or, alternatively, can work in receiver mode where it uses
the built-in handle_key method to accept input passed from a caller.
This module's main function demonstrates both alternatives.
"""

import sys
import string # for string.printable
import util, terminal, keyboard, display

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
    def __init__(self, controller=None, 
                 prompt='', handler=terminal.getchar, do_command=None,
                 startup=None, stopped=None, cleanup=None):
        """
        All arguments are optional, with defaults

        controller - object or module with functions or methods named
        start and stop, used for job control, when this Command instance 
        is multiplexed with other Commands that use the same event.
        Default: None, use when this Command instance is a task on its own,
        with no other jobs contending for the same event.

        prompt - Prompt string that appears at the start of each line.
        Default is empty string '', no prompt.

        handler - function to call to read char(s) to build command
        string. Default is terminal.getchar, could also read/process
        multichar sequence.

        do_command - function to execute command.  Can be any callable
        that takes one argument, a string.  Default None (which crashes).
        command.

        startup - callable to call if needed when application starts
        up or resumes, to initialize display or ...  Default: None,
        this argument is not used by some applications.

        stopped - callable that returns True when application is about
        to exit.  Default: (lambda: True), which causes application to
        exit after one command.   If the stopped argument is provided, it must
        be a callable with one argument, the command string, for example:
        (lambda command: command == keyboard.C_d).  The command argument is 
        provided automatically by code in the body of this class.

        cleanup - callable to call if needed when application exits or
        suspends, to clean up display or ...  Default: None, this
        argument is not used by some applications.
        """
        self.controller = controller
        self.prompt = prompt # string to prompt for command 
        self.handler_body = handler # callable reads char(s) to build command string
        self.do_command_body = do_command # callable that executes command string
        self.startup = startup
        self.stopped = (lambda: (stopped(self.command))) if stopped else (lambda: True)
        self.cleanup = cleanup
        self.command = '' # command string 
        self.point = 0  # index of insertion point in self.command
        self.history = list() # list of previous commands, earliest first
        self.hindex = 0 # index into history
        # prompt used for continuation lines: '...' as long as self.prompt
        self.continuation = '.'*(len(self.prompt)-1) + ' ' 
        # Job commands are not passed to do_command, they are handled here
        self.job_commands = (keyboard.C_d,) # just ^D for now, could add more
        # This instance must test self.pre_empted before it calls self.restart()
        self.pre_empted = False
        # keymap must be an attribute because its values are bound methods.
        # Keys in keymap can be multicharacter sequences, not just single chars
        # Update or reassign keymap to use different keys, methods.
        # Most function names in keymap are same as in GNU readline or Emacs
        self.keymap = {
            # This entry requires special-case handling
            #  because it takes an additional argument: the key
            # Use this function with printing terminals, comment out now:
            #  string.printable: self.self_append_command,
            # This function requires display terminal with cursor addressing:
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
            keyboard.C_d: self.handle_C_d, # exit or self.delete_char
            # keyboard.C_d: self.delete_char
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

    def __call__(self, *args, **kwargs):
        """
        Make this Command instance into a callable so it can be invoked by name from Python.
        Give this job focus and Put this job in the foreground and start it.
        """
        if self.controller: # this might be a standalone job with no controller
            self.controller.start(self) # make this the new foreground job
        self.run(*args, **kwargs)

    # Can't merge this into __call__ above because Session switch() also calls it.
    def run(self, *args, **kwargs):
        'Execute startup function if it exists, then restart handler'
        if self.startup:
            self.startup(*args, **kwargs) 
        if self.restart:
            self.restart()

    def handler(self):
        'Read char, add to key sequence.  If sequence is complete, handle key'
        # might block here in self.handler_body()
        # to avoid blocking, must only call when input is ready for handler_body
        key = self.handler_body() 
        if key:
            self.handle_key(key)

    def handle_key(self, key):
        'Collect command string and dispatch on command'
        # key arg might be single character or a sequence of characters
        if key in string.printable[:-5]: # exclude \t\n\r\v\f at the end
            self.keymap[string.printable](key)
        elif key in self.keymap:
            self.keymap[key]()
        else:
            print(keyboard.bel, end=' ') # sound indicates key not handled
        return key # caller might check for 'q' quit cmd or ...

    def do_command(self):
        'Handle the command, then prepare to collect the next command'
        terminal.set_line_mode() # resume line mode for command output
        print() # print command output on new line
        # Job commands are not passed to application via do_command
        if not self.command in self.job_commands:
            self.do_command_body(self.command)
        # Job commands might be handled by this self.stopped()
        if self.stopped():
            if self.cleanup:
                self.cleanup()
            if self.controller:
                self.controller.switch() 
        elif not self.pre_empted:
      	    self.restart()

    def restart(self):
        'Clear command string, print command prompt, set single-char mode'
        self.command = str()
        self.point = 0
        util.putstr(self.prompt) # prompt does not end with \n
        terminal.set_char_mode()

    # All the other methods are invoked via keymap

    # Methods that work on printing terminals

    def accept_line(self):
        self.history.append(self.command) # save command in history list
        self.hindex = len(self.history)-1
        self.do_command()

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
        """
        ^D: stop if command string is empty, otherwise delete character.
        ^D stop is effective only if job control is also configured to handle ^D
        """
        if not self.command:
            util.putstr('^D') # do_command below sets line mode, advances line
            self.command = keyboard.C_d # so job control can find it
            self.do_command() # so job control can handle it
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

# WARNING 'quit' is just for test in __main__ here.  Just one 'quit' in module
# but there are usually several Command instances per session.
quit = False 

# used as command in __main__
def echo(command):
    'Print command on console, q exits without printing'
    global quit
    if command == 'q':
        quit = True
    else:
        print(command)

c = Command(prompt='> ', do_command=echo, 
            stopped=(lambda command: quit or command == keyboard.C_d))

def main():
    # Note - default handler terminal.getchar can't handle multi-char control seqs
    #  like keyboard.up, down, right, left - use ^P ^N ^F ^B instead
    global quit
    quit = False # earlier invocation might have set it True
    # default do_command echo sets quit=True when command='q', also enable ^D exit
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

if __name__ == '__main__':
    main()
