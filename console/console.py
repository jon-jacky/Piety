"""
console.py - Console class, a wrapper that adapts console applications
 for cooperative multitasking. Collects input string without blocking,
 then passes it to application.  Provides line editing and history
 similar to readline.  Provides hooks for job control.
"""

import sys
import string # for string.printable
import util, terminal, keyboard, display, key

# Keymaps are dicts from keycode string to Console method name string.
# Keycodes in keymap can have multiple chars (for example escape sequences).
# Values are strings not function objects so they can refer to bound methods.

# Most method names in lineedit keymaps are derived from GNU readline or Emacs,
# but line operand is implicit: redraw-current-line is just redraw here etc.
# Also remove confusing 'self', self-insert-char is just insert_char here.
# Retain _char suffix, we might add delete_word, insert_word etc.

printable = 'a' # proxy in keymaps for all printable characters
printing_chars = string.printable[:-5] # exclude \t\n\r\v\f at the end

# This keymap requires a video terminal with cursor addressing.
lineedit_keymap = {
    # insert_char requires special-case handling
    #  because it takes an additional argument: the keycode.
    printable: 'insert_char',

    keyboard.bs: 'backward_delete_char',
    keyboard.delete: 'backward_delete_char',
    keyboard.C_a: 'move_beginning',
    keyboard.C_b: 'backward_char',
    keyboard.C_d: 'delete_char',
    keyboard.C_e: 'move_end',
    keyboard.C_f: 'forward_char',
    keyboard.C_k: 'kill',
    keyboard.C_l: 'redraw',
    keyboard.C_u: 'discard',

    # These keys are multicharacter control sequences
    # require keyboard that sends ANSI control sequences
    # and keyboard reader that handles multicharacter keycodes
    keyboard.right: 'forward_char',
    keyboard.left: 'backward_char',
    }

# These keys are active in ed (etc.) input mode.
# This keymap works on a video terminal or a printing terminal.
stub_insert_keymap = {
    # any keycode that maps to accept_line exits from line entry/editing
    keyboard.cr: 'accept_line', # don't add to history, don't exit
    keyboard.C_c: 'interrupt',
    }

insert_keymap = stub_insert_keymap.copy()
insert_keymap.update(lineedit_keymap)

# These keys are active in ed (etc.) command mode. 
# This command mode keymap requires a video terminal with arrow keys.
command_keys = {
    # Any keycode that maps to accept_command is a command terminator.
    keyboard.cr: 'accept_command', # add to history, possibly exit
    keyboard.C_n: 'next_history',
    keyboard.C_p: 'previous_history',
    keyboard.up: 'previous_history',
    keyboard.down: 'next_history',
}

# These keys have job control function only if they are alone at start of line.
# Otherwise they can have editing function - C_d appears in lineedit_keymap.
job_control_keys = {
    keyboard.C_d: 'ctrl_d',
    keyboard.C_z: 'ctrl_z'
    }

# Combine the keymaps - command mode adds several keys to insert mode,
#  also reassigns method for keyboard.cr (RET key)
# job_control_keys replaces ^D del in insert_keymap with eof and adds ^Z suspend
command_keymap = insert_keymap.copy()
command_keymap.update(command_keys)
command_keymap.update(job_control_keys)

# This keymap works on a printing terminal.
lineedit_tty_keymap = {
    # append_char requires special-case handling
    #  because it takes an additional argument: the key.
    printable: 'append_char',
    # Rudimentary in-line editing, just delete last char in line
    keyboard.bs: 'backward_delete_last_char',
    keyboard.delete: 'backward_delete_last_char',
    # Show the line, useful after several edits
    keyboard.C_l: 'redraw_tty',
    keyboard.C_u: 'discard_tty',
}

insert_tty_keymap = stub_insert_keymap.copy()
insert_tty_keymap.update(lineedit_tty_keymap)

# This command mode keymap works on a printing terminal with no arrow keys.
command_tty_keys = {
    # Any keycode that maps to accept_command is a command terminator.
    keyboard.cr: 'accept_command', # add to history, possibly exit
    keyboard.C_n: 'next_history_tty',
    keyboard.C_p: 'previous_history_tty'
    }

# This combined keymap works on a printing terminal.
command_tty_keymap = insert_tty_keymap.copy()
command_tty_keymap.update(command_tty_keys)
command_tty_keymap.update(job_control_keys)

class Console(object):
    'Wrapper that adapts console applications for cooperative multitasking'

    replaced = False

    def __init__(self, prompt=(lambda: ''), reader=key.Key(),
                 do_command=(lambda command: None),
                 stopped=(lambda command: False),
                 keymap=(lambda: command_keymap),
                 startup=(lambda: None), cleanup=(lambda: None),
                 start=(lambda: None), exit=(lambda: None)):
        """
        All arguments are optional keyword arguments with defaults.

        prompt - callable with no arguments that returns the prompt
        string, which might depend on the state of the application.
        Default returns the empty string (no prompt).

        reader - callable with no arguments to read a keycode, which
        might be a single character or several (an escape sequence,
        for example).  Takes no arguments and returns a keycode, or
        returns empty string '' to indicate char was received but
        keycode is incomplete.  Default is key.Key(), handles single
        characters and a few ANSI escape sequences.

        do_command - callable to execute a command.  Takes one
        argument, the command string.  Default does nothing.

        stopped - callable that returns True when the application
        should stop or exit.  Takes one argument, a string, typically
        the command string, so stopped() can check if command is
        something like 'exit()' or 'quit' - but stopped() might check
        application state instead.  Default returns False, never exits
        (but we can still suspend the application using the
        job_commands arg, below).

        keymap - callable with no arguments that returns the keymap
        for handling both commands and input text.  Keymap contents
        might depend on the application state.  Default returns
        command_keymap defined in this module.

        startup - callable that invokes application code to run
        when application starts up or resumes, for example to
        initialize display. Default does nothing.

        cleanup - callable that invokes application code to run when
        application exits or suspends, for example to clean up
        display.  Default does nothing.

        start - callable that invokes job control code to run when
        application starts up or resumes, for example to place any
        previously running application in the background.  Default
        does nothing.

        exit - callable that invokes job control code to run when
        application exits or suspends, for example to place any
        previously suspended application back in the foreground.
        Default does nothing.
        """
        self.prompt = prompt # can be other prompt or '' in other modes
        self.reader = reader # callable, reads char(s) to build command string 
        self.do_command = (lambda: do_command(self.command))
        self.stopped = (lambda: stopped(self.command))
        self.keymap = keymap
        self.initcommand = '' # command string at the beginning of the cycle
        self.initpoint = None # index into command string at beginnig of cycle
        self.command = self.initcommand
        self.point = self.initpoint  # index into self.command
        self.history = list() # list of previous commands, earliest first
        self.hindex = 0 # index into history
        self.startup = startup # hooks in to application
        self.cleanup = cleanup
        self.start = start # hooks out to job control
        self.exit = exit

    # Piety Session switch method requires job has method named resume
    def resume(self):
        self.startup()
        self.restart()

    def __call__(self):
        self.start()
        self.resume()
        Console.replaced = True

    def stop(self):
        self.restore() # calls print() for newline
        self.cleanup()
        self.exit()

    def run(self):
        """
        Console event loop - run a single Console instance as an application.
        For testing only; handler() blocks, can only run one Console at a time.
        """
        self.__call__()
        while not (self.stopped()
                   or self.command in job_control_keys):
            self.handler() # blocks in self.reader at each character
        self.stop()

    # alternative run_noreader could pass keycode to handler, default getchar

    def reinit(self, command=None, point=None):
        're-initialize command line in self.command'
        self.start_col = len(self.prompt())+1 # 1-based indexing, not 0-based
        self.command = self.command if command is None else command
        self.point = len(self.command) if point is None else point

    def handler(self):
        # Read char, add to keycode sequence.  If seq complete, return keycode
        # To avoid blocking in self.reader(),must only call when input is ready
        # An alternative way would run reader first, pass keycode to handler
        keycode = self.reader() # returns '' when keycode is not yet complete
        # keycode might be single character or a sequence of characters.
        # Printable keys require special-case handling,
        # because their method takes an additional argument: the key itself.
        if keycode in printing_chars:
            method = getattr(self, self.keymap()[printable])
            method(keycode)
        elif keycode in self.keymap():
            method = getattr(self, self.keymap()[keycode])
            method()
        elif keycode:
            util.putstr(keyboard.bel) # sound indicates no handler
        else:
            pass # incomplete keycode, do nothing

    # These keys have job control fcn only if they are alone at start of line.
    # Otherwise they can have editing function - C_d appears in lineedit_keymap.

    def ctrl_d(self):
        if self.command == '':
            self.command = keyboard.C_d # so job control code can find it
            util.putstr('^D')  # no newline, caller handles it.
            self.stop()
        else:
            self.delete_char()

    def ctrl_z(self):
        if self.command == '':
            self.command = keyboard.C_z # so job control code can find it
            print('^Z')
            util.putstr('\rStopped') # still in raw mode, print didn't RET
            self.stop()
        else: 
            util.putstr(keyboard.bel) # sound indicates no handler

    # ^C exit is more drastic than job control, exits to top-level Python

    def interrupt(self):
        'Handle ^C, exit from Python sesson'
        # raw mode terminal doesn't respond to ^C, must handle here
        util.putstr('^C') 
        terminal.set_line_mode() # on new line...
        print()              # ... otherwise traceback is a mess
        raise KeyboardInterrupt

    # The following methods, restore through restart, are invoked by
    # accept_line (when the user finishes entering/editing text in insert mode)
    # or accept_command (when the user finishes entering/editing a command).
    # The user typically indicates this by typing RET, but the actual keycodes
    # (for each mode) are set by keymaps in self.keymap.
    # Complications arise from commands that might exit or suspend application
    # (so control must be transferred elsewhere) and commands that might 
    # initialize the command (or text) line, overriding defaults 
    # (which must be restored later).

    def restore(self):
        'Restore terminal line mode, prepare to print on new line'
        terminal.set_line_mode()
        print()

    def do_command_1(self):
        'Call do_command, but first prepare to restore default command line'
        # initcommand initpoint assigned here, might be reassigned by do_command
        # but are not used until self.restart calls self.reinit
        self.initcommand = '' # default restart value for self.command
        self.initpoint = None  #  "    "   self.point
        self.do_command() # Might assign non-default to initcommand, initpoint.

    # accept_line and accept_command invoke the other methods in this section.
    # These are the commands that are invoked from the keymaps.
    # accept_line is used in insert modes, accept_command in command modes.
    def accept_line(self):
        'For insert modes: handle line, but no history, exit, or job control'
        self.restore()      # advance line and put terminal in line mode 
        self.do_command_1() # might reassign self.mode, self.command
        self.restart()      # print prompt and put term in character mode

    def accept_command(self):
        'For command modes: handle line, with history, exit, and job control'
        self.history.append(self.command)
        self.hindex = len(self.history) - 1
        self.restore()      # advance line and put terminal in line mode 
        self.do_command_1() # might reassign self.command, Console.replaced
        # do_command might invoke job control to suspend or replace application
        if self.stopped():
            self.stop()
        elif not Console.replaced:
            self.restart() # print prompt and put term in character mode
        else:
            Console.replaced = False

    def restart(self):
        'Prepare to collect a command string using the command object.'
        self.reinit(command=self.initcommand, point=self.initpoint)
        util.putstr(self.prompt() + self.command) # command might be empty
        self.move_to_point() # might not be end of line
        terminal.set_char_mode()

    def retrieve_previous_history(self):
        if self.history:
            length = len(self.history)
            self.hindex = self.hindex if self.hindex < length else length-1
            self.initcommand = self.history[self.hindex]
            self.reinit(command=self.initcommand, point=self.initpoint)
        self.hindex = self.hindex - 1 if self.hindex > 0 else 0

    def retrieve_next_history(self):
        length = len(self.history)
        self.hindex = self.hindex + 1 if self.hindex < length else length
        self.initcommand = (self.history[self.hindex] 
                          if self.hindex < length else '')
        self.reinit(command=self.initcommand, point=self.initpoint)

    # Command history, separate methods for video and printing terminals

    def previous_history(self):
        self.retrieve_previous_history()
        self.redraw()

    def next_history(self):
        self.retrieve_next_history()
        self.redraw()

    def previous_history_tty(self):
        self.retrieve_previous_history()
        self.redraw_with_prefix('^P\r\n')

    def next_history_tty(self):
        self.retrieve_next_history()
        self.redraw_with_prefix('^N\r\n')

    # Editing that requires a display terminal with cursor addressing

    def move_to_point(self):
        display.move_to_column(self.start_col + self.point)
 
    def move_beginning(self):
        self.point = 0
        self.move_to_point()

    def move_end(self):
        self.point = len(self.command)
        self.move_to_point()

    def insert_char(self, keycode):
        self.command = (self.command[:self.point] + keycode +
                      self.command[self.point:])
        self.point += 1
        display.insert_char(keycode)

    def backward_delete_char(self):
        if self.point > 0:
            self.command = (self.command[:self.point-1] + self.command[self.point:])
            self.point -= 1
            display.backward_delete_char()

    def backward_char(self):
        if self.point > 0:
            self.point -= 1
            display.backward_char()

    def delete_char(self):
        self.command = (self.command[:self.point] + self.command[self.point+1:])
        display.delete_char() # point does not change

    def forward_char(self):
        if self.point < len(self.command):
            self.point += 1
            display.forward_char()

    def kill(self):
        'delete line from point to end-of-line'
        self.command = self.command[:self.point] # point does not change
        display.kill_line()

    def redraw(self):
        'redraw line'
        # Maybe ^L on vt should refresh whole window or even whole frame?
        display.move_to_column(self.start_col)
        self.point = len(self.command)
        util.putstr(self.command)
        display.kill_line() # remove any leftover text past self.command

    def discard(self): # name like gnu readline unix-line-discard
        'discard line'
        self.command = str() 
        self.move_beginning() # accounts for prompt, assigns point
        display.kill_line() # erase from cursor to end of line

    # Editing that works on printing terminals

    def append_char(self, keycode):
        self.command += keycode
        self.point += 1
        util.putstr(keycode)

    def backward_delete_last_char(self):
        if self.point > 0:
            ch = self.command[-1]
            self.command = self.command[:-1]
            self.point -= 1
            # util.putstr('^H') # omit, it is more helpful to echo
            util.putstr('\\%s' % ch) # echo \c where c is deleted char

    def discard_tty(self): # name like gnu readline unix-line-discard
        'discard entire line including prompt on printing terminal'
        self.command = ''
        util.putstr('^U\r\n' + self.prompt())  # prompt on new line

    def redraw_with_prefix(self, prefix):
        'redraw entire line with prefix and prompt on printing terminal'
        util.putstr(prefix + self.prompt())
        self.redraw()

    def redraw_tty(self):
        'redraw entire line including prompt on printing terminal'
        self.redraw_with_prefix('^L\r\n')

# Test: echo input lines, use job control commands ^D ^Z to exit.
echo = Console(prompt=(lambda: '> '), 
               do_command=(lambda command: print(command)))

def main():
    echo.run()

if __name__ == '__main__':
    main()
