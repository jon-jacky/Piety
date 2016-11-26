"""
console.py - Console class, skeleton command line application.  

Collects a command (string), with editing and history, and passes it
  to a handler (callable) to execute.

Collects the string one character at a time, so this class can be used 
  in a cooperative multitasking system without blocking.

Delegates in-line editing of the command string to another class.  A
  minimal stub class with rudimentary editing is included in this module.

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
import lineinput, key # used in Console __init__ defaults

# A keymap is a dictionary from keycode string to Console method name string.
# Keycodes in keymap can have multiple characters (for example escape sequences)
# Values are name strings not function objects. They can refer to bound methods.
# Most method names in the keymap are the same as in GNU readline or Emacs.

printable = 'a' # proxy in keymaps for all printable characters
printing_chars = string.printable[:-5] # exclude \t\n\r\v\f at the end

# This keymap works for ed insert mode on a printing terminal.
# (These keys are also enabled in ed command mode.)
printing_insertmode_keymap = {
    # any keycode that maps to accept_line is a command terminator
    keyboard.cr: 'accept_line', # don't add to history, don't exit
    keyboard.C_c: 'interrupt',
    keyboard.C_l: 'redraw_current_line_tty',
    keyboard.C_u: 'line_discard_tty',
    }

# Add keys used in ed command mode on a printing terminal.
printing_command_keys = {
    # any keycode that maps to accept_line is a command terminator
    keyboard.cr: 'accept_command', # add to history, possibly exit
    keyboard.C_n: 'next_history_tty',
    keyboard.C_p: 'previous_history_tty',
    }

# This combined keymap works for ed command mode on a printing terminal.
printing_keymap = printing_insertmode_keymap.copy()
printing_keymap.update(printing_command_keys)

# This keymap works for ed insert mode on a terminal with cursor addressing
# (These keys are also enabled in ed command mode.)
vt_insertmode_keymap = {
    # any keycode that maps to accept_line is a command terminator
    keyboard.cr: 'accept_line', # don't add to history, don't exit
    keyboard.C_c: 'interrupt',
    # Put these next two entries in LineInput keymap, not here
    # keyboard.C_l: 'redraw_current_line',
    # keyboard.C_u: 'line_discard',
    }

# Add keys used in ed command mode on a terminal with cursor addressing
#  and arrow keys
vt_command_keys = {
    # any keycode that maps to accept_command is a command terminator
    keyboard.cr: 'accept_command', # add to history, possibly exit
    keyboard.C_n: 'next_history',
    keyboard.C_p: 'previous_history',
    keyboard.up: 'previous_history',
    keyboard.down: 'next_history',
    }

# This combined keymap works for ed command mode
#  on a terminal with cursor addressing and arrow keys
vt_keymap = vt_insertmode_keymap.copy()
vt_keymap.update(vt_command_keys)

# For now, job control commands must be single keycodes at start of empty line.
# Job keymap is checked before ordinary keymap so same keys can appear in both.
job_commands_keymap = {
    keyboard.C_d: 'ctrl_d',
    keyboard.C_z: 'ctrl_z'
}

class LineInput(object):
    """
    Minimal but usable class for default command object.
    Works on printing terminal, only editing is backspace key.
    """
    def __init__(self, keymap={c: None for c in 
                               printing_chars + keyboard.delete}):
        self.reinit()
        self.keymap = keymap

    def reinit(self, line='', prompt='', point=None):
        self.line = line
        self.point = point if point != None else len(self.line) # end of line
        self.start_col = len(prompt)+1 # 1-based indexing, not 0-based

    def handler(self, keycode):
        'No keymap lookup, just two simple cases: append char or delete last'
        if keycode == keyboard.delete and self.line: # edit with delete
            ch = self.line[-1]
            self.line = self.line[:-1] # delete last char
            util.putstr('\\%s' % ch) # echo \c where c is deleted char
        else: # keymap ensures this is printing char
            util.putstr(keycode)  # just echo ... 
            self.line += keycode # ... and append char

    # This is required, it is called by Console class restart method.
    # Here it does nothing, just leaves cursor where preceding putstr left it.
    def move_to_point(self):
        pass

class Console(object):
    def __init__(self, prompt='', reader=key.Key(),
                 command=lineinput.LineInput(),
                 do_command=(lambda command: None),
                 stopped=(lambda command: False),
                 keymap=vt_keymap, 
                 job_commands=job_commands_keymap,
                 mode=(lambda: True),
                 # False means not command mode: empty prompt, insert mode 
                 behavior={ False: ('', vt_insertmode_keymap) }):
        """
        All arguments are optional, with defaults.  Defaults were chosen
         to simplify the editors ed, edsel, and eden.  For many applications,
         it should only be necessary to specify these arguments: prompt,
         do_command, stopped, and mode.

        prompt - Prompt string, appears unless overidden by mode and 
          behavior args (below).  
         Default is empty string '', no prompt.

       reader - callable to read a keycode, which might be a single
         character or several (an escape sequence, for example).
         Takes no arguments and returns a keycode, or returns empty
         string '' to indicate char was received but keycode is
         incomplete.
        Default is terminal.getchar, always gets a single character.

        command - object to collect and store command line, with
          in-line editing.  
         Default is instance of lineinput.LineInput class, which
          requires a video terminal.  For printing terminals, use the
          mininal LineInput class defined in this module.

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

        keymap - dictionary from keycode to Console method name
          string, used except in modes where it is overridden by mode
          and behavior args (below).
         Default: vt_keymap (defined above in this module), requires
          video terminal.

        job_commands: dictionary from keycode to job control method
          name string.  The method typically bypasses or suspends the
          application.  Job control keycodes are only effective when
          they appear alone at the beginning of an empty command line,
          so they can be the same as keycodes in keymap.  For example
          the job control exit command ^D is the same as the LineInput
          delete character command ^D.  
         Default: job_commands_keymap (defined in this module),
          entries for ^D and ^Z that suspend the application.

        mode - callable to get current application mode, returns a
          value (of some type) that depends on the application.  Used
          with behavior argument (below) to select prompt and keymap.
         Default: (lambda: True), always use prompt and keymap args
          (above).

        behavior - Customizes prompt and keymap for mode.  A dictionary
          indexed by values returned by calling mode() (above).  Each
          key in the dict (a mode) is associated with a tuple:
          (prompt, keymap) to use in that mode.  
         Default is { False: ('', vt_insertmode_keymap) }, works with
          ed (etc.) insert mode (when self.mode() returns True for command
          mode, False for insert mode)
        """
        self.default_prompt = prompt # prompt string used in command mode
        self.prompt = prompt # can be other prompt or '' in other modes
        self.reader = reader # callable, reads char(s) to build command string
        self.appending = True # False to update lines already on display
        self.mode = mode
        self.behavior = behavior
        self.command = command
        # Assign default restart values for self.command.line, point.
        # Some do_command might assign non-default values.
        self.initline = ''
        self.initpoint = None
        self.reinit_command() # assign initline, initpoint, prompt
        self.do_command = (lambda: do_command(self.command.line))
        self.stopped = (lambda: stopped(self.command.line))
        self.job = None  # assign elsewhere, then here use self.job.stop() etc.
        self.history = list() # list of previous commands, earliest first
        self.hindex = 0 # index into history
        self.default_keymap = keymap # keymap used in command mode
        self.keymap = keymap # can be other keymap in other modes
        self.job_commands = job_commands

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
            if self.job:
                self.job.do_stop() # callback to job control
            return
        elif keycode and keycode in self.keymap:
            method = getattr(self, self.keymap[keycode])
            method()
        elif keycode and (keycode in printing_chars or 
                          keycode in self.command.keymap):
            self.command.handler(keycode)
        elif keycode:
            print(keyboard.bel, end=' ') # sound indicates key not handled
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
    # (for each mode) are set by keymaps in self.keymap and self.behavior.
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
        # but are not used until self.restart calls self.reinit_command.
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
            if self.job:
                self.job.do_stop() # callback to job control
            else:
                return  # no job - just exit application
        elif self.job and self.job.replaced: # command may replace or stop app
            return
        else:
            self.restart() # print prompt and put term in character mode
            return # application continues

    def reinit_command(self):
        'Pass previously assigned attributes to self.command.reinit'
        self.command.reinit(line=self.initline, point=self.initpoint,
                                 prompt=self.prompt)

    def restart(self):
        """
        Prepare to collect a command string using the command object.
        Assign prompt and keymap for current mode.
        Assign initial command string (default empty) for in-line editing.
        Print command prompt and command line (if any), set single-char mode.
        """
        mode = self.mode() # do_command may have changed mode
        if mode in self.behavior:
            self.prompt, self.keymap = self.behavior[mode]
        else:
            self.prompt, self.keymap = self.default_prompt, self.default_keymap
        # Re-initialize command object with previously assigned attributes.
        # Only now do we have self.prompt to accompany initline and initpoint.
        self.reinit_command() # maybe not the usual default empty line
        if self.appending: # True to add line to display, False update in place
            util.putstr(self.prompt + self.command.line) # might be empty
        self.command.move_to_point() # might not be end of line
        terminal.set_char_mode()

    # Command history, works on printing terminals

    def retrieve_previous_history(self):
        if self.history:
            length = len(self.history)
            self.hindex = self.hindex if self.hindex < length else length-1
            self.initline = self.history[self.hindex]
            self.reinit_command()
        self.hindex = self.hindex - 1 if self.hindex > 0 else 0

    def previous_history_tty(self):
        self.retrieve_previous_history()
        util.putstr('^P\r\n' + self.prompt + self.command.line)

    def retrieve_next_history(self):
        length = len(self.history)
        self.hindex = self.hindex + 1 if self.hindex < length else length
        self.initline = (self.history[self.hindex] 
                          if self.hindex < length else '')
        self.reinit_command()

    def next_history_tty(self):
        self.retrieve_next_history()
        util.putstr('^N\r\n' + self.prompt + self.command.line)

    # Command history, requires video terminal.

    def previous_history(self):
        self.retrieve_previous_history()
        self.command.redraw_current_line()

    def next_history(self):
        self.retrieve_next_history()
        self.command.redraw_current_line()

    # Command editing, works with printing terminal.

    def redraw_current_line_tty(self):
        util.putstr('^L\r\n' + self.prompt)  # on new line
        util.putstr(self.command.line)

    def line_discard_tty(self): # name like gnu readline unix-line-discard
        self.command.line = ''
        util.putstr('^U\r\n' + self.prompt)

    # Command editing that requires a video terminal
    # is not provided by the this class - use LineInput for that.

# Test: echo input lines, use job control commands ^D ^Z to exit.
echo = Console(prompt='> ', do_command=(lambda command: print(command)))

if __name__ == '__main__':
    echo.run()
