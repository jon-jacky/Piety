"""
console.py - Console class, skeleton command line application.  

Collects a command (string), with editing and history, and passes it
  to a handler (callable) to execute.

Collects the string one character at a time, so this class can be used 
  in a cooperative multitasking system without blocking.

Delegates in-line entry and editing of the command string to another class.

Provides command history similar to readline.

Provides for customization by assigning keymaps that map keycodes to
  behaviors.

Provides for modes that assign different keymaps to select different
  behaviors, for example an editor's command and insert modes.

Provides for transferring control when the application exits, or when
  job control commands bypass or suspend the application.

This module has some similar motivations to the Python standard
  library cmd module, but does not provide the same API.
"""

import sys
import string # for string.printable
import util, terminal, keyboard
import inputline, key # define classes used in Console __init__

# These keymaps are dicts from keycode string to Console method name string.
# Keycodes in keymap can have multiple characters (for example escape sequences).
# Values are name strings not function objects so they can refer to bound methods
# Keymaps in this console module are just for controlling commands and jobs
# Keymaps for entering and editing text are in the inputline module

# These keys are active in insert mode - just accept line and interrupt

# This keymap works on a vt terminal or a printing terminal
insert_keymap = {
    # any keycode that maps to accept_line exits from line entry/editing
    keyboard.cr: 'accept_line', # don't add to history, don't exit
    keyboard.C_c: 'interrupt',
    }

# These keys are active in command mode note - we add history keys
# This command mode keymap requires a video terminal with arrow keys
command_keys = {
    # any keycode that maps to accept_command is a command terminator
    keyboard.cr: 'accept_command', # add to history, possibly exit
    keyboard.C_n: 'next_history',
    keyboard.C_p: 'previous_history',
    keyboard.up: 'previous_history',
    keyboard.down: 'next_history',
    }

# Combine the keymaps - commandmode adds several keys to insert mode
# also reassigns method for keyboard.cr (RET key)
command_keymap = insert_keymap.copy()
command_keymap.update(command_keys)

# This command mode keymap works on a printing terminal with no arrow keys
command_tty_keys = {
    # any keycode that maps to accept_command is a command terminator
    keyboard.cr: 'accept_command', # add to history, possibly exit
    keyboard.C_n: 'next_history_tty',
    keyboard.C_p: 'previous_history_tty'
    }

# This combined keymap works on a printing terminal.
command_tty_keymap = insert_keymap.copy()
command_tty_keymap.update(command_tty_keys)

# For now, job control commands must be single keycodes at start of empty line.
# Job keymap is checked before ordinary keymap so same keys can appear in both.
job_commands_keymap = {
    keyboard.C_d: 'ctrl_d',
    keyboard.C_z: 'ctrl_z'
}

printable = 'a' # proxy in keymaps for all printable characters
printing_chars = string.printable[:-5] # exclude \t\n\r\v\f at the end

class Console(object):
    def __init__(self, prompt='', reader=key.Key(),
                 do_command=(lambda command: None),
                 stopped=(lambda command: False),
                 command_keymap=command_keymap, 
                 edit_keymap=inputline.keymap,
                 job_commands=job_commands_keymap,
                 mode=(lambda: True), specialmodes=None):
        """
        All arguments are optional, with defaults.  Defaults were chosen
         to simplify the editors ed, edsel, and eden.  For many applications,
         it should only be necessary to specify these arguments: prompt,
         do_command, stopped, and mode.

        prompt - Prompt string, appears unless overidden by mode and 
          specialmodes args (below).  
         Default is empty string '', no prompt.

       reader - callable to read a keycode, which might be a single
         character or several (an escape sequence, for example).
         Takes no arguments and returns a keycode, or returns empty
         string '' to indicate char was received but keycode is
         incomplete.
        Default is key.Key(), handles single characters and a few ANSI
         escape sequences

        do_command - callable to execute command string.  Takes one
           argument, a string.  
          Default is (lambda command: None), do nothing.

        stopped - callable to test when the application should stop or
          exit.  Takes one argument, a string.  Typically this is the
          command string, so stopped() can check if command is
          something like 'exit()' or 'quit' - but stopped() might
          ignore this string and check some state variable instead.
         Default is (lambda command: False), never exit -- but
          can still suspend application using job_commands (below).

        command_keymap - dictionary from keycode to Console method name
          string, used except in modes where it is overridden by mode
          and specialmodes args (below).  Typically used in command modes.
         Default: command_keymap (defined above in this module)

        job_commands: dictionary from keycode to job control method
          name string.  The method typically bypasses or suspends the
          application.  Job control keycodes are only effective when
          they appear alone at the beginning of an empty command line,
          so they can be the same as keycodes in keymap.  For example
          the job control exit command ^D is the same as the InputLine
          delete character command ^D.  
         Default: job_commands_keymap (defined in this module),
          entries for ^D and ^Z that suspend the application.

        mode - callable to get current application mode, returns a
          value (of some type) that depends on the application.  For
          example, (lambda: ed.command_mode) returns True for ed
          command mode and False for ed insert mode.  Used with
          specialmodes argument (below) to select prompt and keymap.
         Default: (lambda: True), always command mode, use prompt and
          command_keymap args (above).

        specialmodes - Customizes prompt and keymap for mode.  A dictionary
          indexed by the values returned by calling mode() (above).  Each
          key in the dict (a mode) is associated with a tuple:
          (prompt, keymap) to use in that mode.  
         Default is None, which selects { False: ('', insert_keymap) }.
          This works with (for example) ed insert mode.
        """
        # initialize attributes from __init__ arguments
        self.default_prompt = prompt # prompt string used in command mode
        self.prompt = prompt # can be other prompt or '' in other modes
        self.reader = reader # callable, reads char(s) to build command string 
        self.do_command = (lambda: do_command(self.command.line))
        self.stopped = (lambda: stopped(self.command.line))
        self.job_commands = job_commands
        self.keymap = command_keymap
        self.mode = mode
        # call this arg specialmodes because othermodes=None is misleading
        self.othermodes = ({ False: ('', insert_keymap) }
                           if specialmodes is None else specialmodes)
        # initialize other attributes
        self.initline = ''    # some do_command might assign ...
        self.initpoint = None # ..non-default values for initial command string
        self.command=inputline.InputLine(prompt=self.prompt, 
                                         line=self.initline,
                                         point=self.initpoint,
                                         keymap=edit_keymap) # __init__ arg
        self.history = list() # list of previous commands, earliest first
        self.hindex = 0 # index into history
        # We might assign some job controller object to supervisor later.
        # if not None, supervisor must be an object with a method stop(self)
        # and a Boolean attribute named 'replaced'.
        self.supervisor = None  
                                 
    def run(self):
        'Console event loop - run Console instance as an application'
        self.restart()
        while (not self.stopped() and 
               self.command.line not in self.job_commands):
            self.handler() # blocks in self.reader at each character
        self.restore()

    # alternative run_noreader passes keycode to handler, use getchar as default

    def handler(self):
        'Read char, add to keycode sequence.  If seq complete, handle keycode'
        # to avoid blocking in self.reader(), must only call when input is ready
        keycode = self.reader() # returns '' when keycode is not yet complete
        # keycode might be single character or a sequence of characters.
        # Check job keymap before ordinary keymap, same keys can appear in both.
        # Job control commands must be a single keycode at start of line.
        if keycode and (keycode in self.job_commands 
                        and self.command.line == ''):
            self.command.line = keycode # so job control code can find it
            method = getattr(self, self.job_commands[keycode])
            method()
            # For now, all job control commands exit
            self.restore()     # calls print() for newline
            if self.supervisor:
                self.supervisor.stop() # callback to job control
            return
        elif keycode and keycode in self.keymap:
            method = getattr(self, self.keymap[keycode])
            method()
        elif keycode and (keycode in printing_chars or 
                          keycode in self.command.keymap):
            self.command.handler(keycode)
        elif keycode:
            util.putstr(keyboard.bel) # sound indicates key not handled
        else:
            pass # incomplete keycode, do nothing

    # Job control commands, suspend application via self.job_commands, 
    # Two for now just to show we can distinguish commands.

    def ctrl_d(self):
        util.putstr('^D')  # no newline, caller handles it.

    def ctrl_z(self):
        print('^Z')
        util.putstr('\rStopped') # still in raw mode, print didn't RET

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
    # (for each mode) are set by keymaps in self.keymap and self.othermodes.
    # Complications arise due to commands that might exit or suspend application
    # (so control must be transferred elsewhere) and commands that might 
    # initialize the command (or text) line, overriding defaults 
    # (which must be restored later).

    def restore(self):
        'Restore terminal line mode, prepare to print on new line'
        terminal.set_line_mode()
        print()

    def do_command_1(self):
        'Call do_command, but first prepare to restore default command line'
        # initline initpoint assigned here, might be reassigned by do_command
        # but are not used until self.restart calls self.command.reinit
        self.initline = '' # default restart value for self.command.line
        self.initpoint = None  #  "    "   self.point
        self.do_command() # Might assign non-default to initline, initpoint.

    # accept_line and accept_command invoke the other methods in this section.
    # These are the commands that are invoked from the keymaps.
    # accept_line is used in text insert modes, accept_command in command modes.

    def accept_line(self):
        'For ed insert mode: handle line, but no history, exit, or job control'
        self.restore()      # advance line and put terminal in line mode 
        self.do_command_1() # might reassign self.mode, self.command.line
        self.restart()      # print prompt and put term in character mode

    def accept_command(self):
        'For ed command mode: handle line, with history, exit, and job control'
        self.history.append(self.command.line)
        self.hindex = len(self.history) - 1
        self.restore()      # advance line and put terminal in line mode 
        self.do_command_1() # might reassign self.mode, self.command.line
        # do_command might exit or invoke job control to suspend application
        if self.stopped():
            if self.supervisor:
                self.supervisor.stop() # callback to job control
            else:
                return  # no job - just exit application
        elif self.supervisor and self.supervisor.replaced: 
            return # command may replace or stop app
        else:
            self.restart() # print prompt and put term in character mode
            return # application continues

    def restart(self):
        """
        Prepare to collect a command string using the command object.
        Assign prompt and keymap for current mode.
        Assign initial command string (default empty) for in-line editing.
        Print command prompt and command line (if any), set single-char mode.
        """
        mode = self.mode() # do_command may have changed mode
        if mode in self.othermodes:
            self.prompt, self.keymap = self.othermodes[mode]
        else:
            self.prompt, self.keymap = self.default_prompt, command_keymap
        # Re-initialize command object with previously assigned attributes.
        # Only now do we have self.prompt to accompany initline and initpoint.
        self.command.reinit(prompt=self.prompt, line=self.initline, 
                            point=self.initpoint)
        util.putstr(self.prompt + self.command.line) # might be empty
        self.command.move_to_point() # might not be end of line
        terminal.set_char_mode()

    def retrieve_previous_history(self):
        if self.history:
            length = len(self.history)
            self.hindex = self.hindex if self.hindex < length else length-1
            self.initline = self.history[self.hindex]
            self.command.reinit(prompt=self.prompt, line=self.initline, 
                                point=self.initpoint)
        self.hindex = self.hindex - 1 if self.hindex > 0 else 0

    def retrieve_next_history(self):
        length = len(self.history)
        self.hindex = self.hindex + 1 if self.hindex < length else length
        self.initline = (self.history[self.hindex] 
                          if self.hindex < length else '')
        self.command.reinit(prompt=self.prompt, line=self.initline, 
                            point=self.initpoint)

    # Command history, separate methods for video and printing terminals

    def previous_history(self):
        self.retrieve_previous_history()
        self.command.redraw()

    def next_history(self):
        self.retrieve_next_history()
        self.command.redraw()

    def previous_history_tty(self):
        self.retrieve_previous_history()
        self.command.redraw_with_prefix('^P\r\n')

    def next_history_tty(self):
        self.retrieve_next_history()
        self.command.redraw_with_prefix('^N\r\n')


# Test: echo input lines, use job control commands ^D ^Z to exit.
echo = Console(prompt='> ', do_command=(lambda command: print(command)))

if __name__ == '__main__':
    echo.run()
