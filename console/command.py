"""
command.py - Command class, skeleton command line application.  

Collects a command (string), with editing and history, and passes it
  to a handler (callable) to execute.

Collects the string one character at a time, so this class can be used 
  for cooperative multitasking without blocking.

Delegates in-line editing of the command string to another class.  A
  minimal  stub class with rudimentary editing is included in this module.

Provides command history similar to readline.

Provides for customization by assigning keymaps that map keycodes to
  behaviors.

Provides for modes that assign different keymaps to select different
  behaviors, for example an editor's command and insert modes.

Provides for job control commands that can bypass or suspend the
  application.

This module has some similar motivations to the Python standard
  library cmd module, but does not provide the same API.
"""

import sys
import string # for string.printable
import util, terminal, keyboard

# A keymap is a dictionary from keycode string to Command method name string.
# Keycodes in keymap can have multiple characters (for example escape sequences)
# Values are name strings not function objects. They can refer to bound methods.
# Most method names in the keymap are the same as in GNU readline or Emacs.

printable = 'a' # proxy in keymaps for all printable characters
printing_chars = string.printable[:-5] # exclude \t\n\r\v\f at the end

# Any keycode that maps to accept_line or _command is a command terminator

# This keymap works for ed insert mode on a printing terminal.
# (These keys are also enabled in ed command mode.)
printing_insert_keymap = {
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
printing_keymap = printing_insert_keymap.copy()
printing_keymap.update(printing_command_keys)

# This keymap works for ed insert mode on a terminal with cursor addressing
# (These keys are also enabled in ed command mode.)
vt_insert_keymap = {
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
    # any keycode that maps to accept_line is a command terminator
    keyboard.cr: 'accept_command', # add to history, possibly exit
    keyboard.C_n: 'next_history',
    keyboard.C_p: 'previous_history',
    keyboard.up: 'previous_history',
    keyboard.down: 'next_history',
    }

# This combined keymap works for ed command mode
#  on a terminal with cursor addressing and arrow keys
vt_keymap = vt_insert_keymap.copy()
vt_keymap.update(vt_command_keys)

# For now, job control commands must be single keycodes at start of empty line.
# Job keymap is checked before ordinary keymap so same keys can appear in both.
job_control_keymap = {
    keyboard.C_d: 'ctrl_d',
    keyboard.C_z: 'ctrl_z'
}

class LineInput(object):
    """
    Minimal but usable class for default command_line object.
    Works on printing terminal, only editing is backspace key.
    """
    def __init__(self, keymap={c: None for c in 
                               printing_chars + keyboard.delete}):
        self.chars = ''  # string to edit
        self.start_col = 1   # index of first column on display, 1-based
        self.keymap = keymap
        self.point = 0 # not used here, but assigned by Command restart etc.

    def handler(self, keycode):
        'No keymap lookup, just two simple cases: append char or delete last'
        if keycode == keyboard.delete and self.chars: # edit with delete
            ch = self.chars[-1]
            self.chars = self.chars[:-1] # delete last char
            util.putstr('\\%s' % ch) # echo \c where c is deleted char
        else: # keymap ensures this is printing char
            util.putstr(keycode)  # just echo ... 
            self.chars += keycode # ... and append char

    # This is required, it is called by Command class restart method.
    # It does nothing, just leaves the cursor where preceding putstr left it.
    def move_to_point(self):
        pass

class Command(object):
    def __init__(self, prompt='', reader=terminal.getchar, 
                 command_line=LineInput(),
                 do_command=(lambda command: None),
                 stopped=(lambda command: False),
                 # this default keymap works with default command_line
                 keymap=printing_keymap, 
                 job_control=job_control_keymap,
                 mode=(lambda: True), behavior={}):
        """
        All arguments are optional, with defaults.

        prompt - Prompt string, appears unless overidden by mode and 
          behavior args (below).  
         Default is empty string '', no prompt.

       reader - callable to read a keycode, which might be a single
         character or several (an escape sequence, for example).
         Takes no arguments and returns a keycode, or returns empty
         string '' to indicate char was received but keycode is
         incomplete.
        Default is terminal.getchar, always gets a single character.

        command_line - object to collect and store command line, and
           in-line editing.  Default is instance of minimal LineInput
           class defined in this module, which works on a printing
           terminal.
          Some Command methods require self.command_line to belong to
           a richer class that provides video cursor addressing.  The
           lineinput module provides a suitable LineInput class.
          You must ensure that the keymap and behavior arguments
           (described below) only contain methods that can be 
           executed by the command_line class you have have assigned.

        do_command - callable to execute command string.  Takes one
           argument, a string.  
          Default is (lambda command: None), do nothing.

        stopped - callable to test when the application should stop or
          exit.  Takes one argument, a string.  Typically this is the
          command string, so stopped() can check if command is
          something like 'exit()' or 'quit' - but stopped() might
          ignore this string and check some state variable instead.
         Default is (lambda command: False), never exit.

        keymap - dictionary from keycode to Command method name
          string, used except in modes where it is overridden by mode
          and behavior args (below).
         Default: vt_keymap (defined above in this module)

        job_control: dictionary from keycode to job control method
          name string.  The method typically bypasses or suspends the
          application.  Job control keycodes are only effective when
          they appear alone at the beginning of an empty command line,
          so they can be the same as keycodes in keymap.  For example
          the job control exit command ^D is the same as the LineInput
          delete character command ^D.  
         Default: entries for ^D and ^Z that suspend the application.

        mode - callable to get current application mode, returns a
          value (of some type) that depends on the application.  Used
          with behavior argument (below) to select prompt and keymap.
         Default: (lambda: True), always use prompt and keymap args
          (above).

        behavior - Customizes prompt and keymap for mode.  A dictionary
          indexed by values returned by calling mode() (above).  Each
          key in the dict (a mode) is associated with a tuple:
          (prompt, keymap) to use in that mode.  
         Default is {}, the empty dictionary, always use prompt
          and keymap args (above).
        """
        self.default_prompt = prompt # prompt string used in command mode
        self.prompt = prompt # can be other prompt or '' in other modes
        self.reader = reader # callable, reads char(s) to build command string
        self.mode = mode
        self.behavior = behavior
        self.command_line = command_line
        self.command_line.chars = ''
        self.command_line.start_col = len(self.prompt) + 1 # 1-based not 0-based
        self.clear_chars = True # do_command might assign False
        self.do_command = (lambda: do_command(self.command_line.chars))
        self.stopped = (lambda: stopped(self.command_line.chars))
        self.job = None  # assign elsewhere, then here use self.job.stop() etc.
        self.history = list() # list of previous commands, earliest first
        self.hindex = 0 # index into history
        self.default_keymap = keymap # keymap used in command mode
        self.keymap = keymap # can be other keymap in other modes
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
        """
        Prepare to collect a command string using the command_line object.
        Assign prompt and keymap for current mode.
        Print command prompt, set single-char mode.
        Do NOT initialize chars and point, caller has assigned them already
        """
        mode = self.mode() 
        if mode in self.behavior:
            self.prompt, self.keymap = self.behavior[mode]
        else:
            self.prompt, self.keymap = self.default_prompt, self.default_keymap
        self.command_line.start_col = len(self.prompt) + 1 # 1-based not 0-based
        util.putstr(self.prompt + self.command_line.chars)
        self.command_line.move_to_point() # might not be end of line
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

    def accept_chars(self):
        """
        Used by both accept_line and accept_command, below.
        Makes it possible for do_command to optionally initialize command_line.
        """
        self.restore()    # advance line and put terminal in line mode 
        self.clear_chars = True # do_command might assign this False
        self.do_command() # do_command might assign chars, point, clear_chars
        if self.clear_chars: # if do_command did not assign chars = False
            self.command_line.chars = ''
            self.command_line.point = 0

    # Application commands invoked via keymap

    def accept_line(self):
        'For ed insert mode: handle line, but no history, exit, or job control'
        self.accept_chars()
        self.restart() # print prompt and put term in character mode

    def accept_command(self):
        'For ed command mode: handle line, with history, exit, and job control'
        self.history.append(self.command_line.chars) # save command in history
        self.hindex = len(self.history)-1
        self.accept_chars()
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

    def interrupt(self):
        'Handle ^C, exit from Piety'
        # raw mode terminal doesn't respond to ^C, must handle here
        util.putstr('^C') 
        terminal.set_line_mode() # on new line...
        print()              # ... otherwise traceback is a mess
        raise KeyboardInterrupt

    # Command history, works with default command_line on printing terminals

    def retrieve_previous_history(self):
        if self.history:
            length = len(self.history)
            self.hindex = self.hindex if self.hindex < length else length-1
            self.command_line.chars = self.history[self.hindex]
        self.hindex = self.hindex - 1 if self.hindex > 0 else 0

    def previous_history_tty(self):
        self.retrieve_previous_history()
        util.putstr('^P\r\n' + self.prompt + self.command_line.chars)

    def retrieve_next_history(self):
        length = len(self.history)
        self.hindex = self.hindex + 1 if self.hindex < length else length
        self.command_line.chars = (self.history[self.hindex] 
                                   if self.hindex < length else '')

    def next_history_tty(self):
        self.retrieve_next_history()
        util.putstr('^N\r\n' + self.prompt + self.command_line.chars)

    # Command history, requires command_line that uses video terminal.

    def previous_history(self):
        self.retrieve_previous_history()
        self.command_line.point = len(self.command_line.chars)
        self.command_line.redraw_current_line()

    def next_history(self):
        self.retrieve_next_history()
        self.command_line.point = len(self.command_line.chars)
        self.command_line.redraw_current_line()

    # Command editing, works with default command_line on printing terminal.

    def redraw_current_line_tty(self):
        util.putstr('^L\r\n' + self.prompt)  # on new line
        util.putstr(self.command_line.chars)

    def line_discard_tty(self): # name like gnu readline unix-line-discard
        self.command_line.chars = ''
        util.putstr('^U\r\n' + self.prompt)

    # Command editing, requires video terminal with cursor addressing,
    # not provided in this module, see (for example) lineinput module.

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
    # Default handler terminal.getchar can't handle multi-char control
    # sequences like keyboard.up, down, right, left - use ^P ^N ^F ^B instead
    c.restart()
    while c.command_line.chars not in c.job_control: # use job control for exit
        # Here Command instance works in reader mode:
        # uses the function passed to its handler argument to read its input.
        c.handler()
        # Alternatively, here Command instance works in receiver mode:
        # uses its built-in dispatch method to accept input passed by caller.
        # To demonstrate, comment out previous line and uncomment these lines:
        #char = terminal.getchar()
        #c.handler(char)
    c.restore()

if __name__ == '__main__':
    # default()
    main()
