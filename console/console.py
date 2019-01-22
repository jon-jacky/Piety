"""
console.py - Console class, a wrapper that adapts console applications
 for cooperative multitasking. Collects input string without blocking,
 then passes it to application.  Provides line editing and history
 similar to readline.  Provides hooks for job control.
"""

import sys, string
import util, terminal, keyboard, display, key
from piety import State

# used by keymaps, below
printable = 'a' # proxy in keymaps for all printable characters
printing_chars = string.printable[:-5] # exclude \t\n\r\v\f at the end

class Console(object):
    'Wrapper that adapts console applications for cooperative multitasking'
    def __init__(self, name=__module__,
                 prompt=(lambda: ''), reader=key.Key(),
                 process_line=(lambda line: None),
                 stopped=(lambda line: False),
                 startup=(lambda: None), cleanup=(lambda: None),
                 start=(lambda: None), exit=(lambda: None)):
        """
        All arguments are optional keyword arguments with defaults.

        name - string that names this instance, default __module__,
        that is 'console'.  Useful when jobs are listed, etc.

        prompt - callable with no arguments that returns the prompt
        string, which might depend on the state of the application.
        Default returns the empty string (no prompt).

        reader - callable with no arguments to read a keycode, which
        might be a single character or several (an escape sequence,
        for example).  Takes no arguments and returns a keycode, or
        returns empty string '' to indicate char was received but
        keycode is incomplete.  Default is key.Key(), handles single
        characters and a few ANSI escape sequences.

        process_line - callable to process a line, for example to
        execute a command or add text to a buffer.  Takes one
        argument, the line.  Default does nothing.

        stopped - callable that returns True when the application
        should stop or exit.  Takes one argument, a string, typically
        the command string, so stopped() can check if command is
        something like 'exit()' or 'quit' - but stopped() might check
        application state instead.  Default returns False, never exits.

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
        self.name = name
        self.prompt = prompt # can be other prompt or '' in other modes
        self.reader = reader # callable, reads char(s) to build line 
        self.process_line = (lambda: process_line(self.line))
        self.stopped = (lambda: stopped(self.line))
        self.line = '' # empty line at beginning of cycle
        self.point = 0 # index into self.line at beginning of cycle
        self.start_col = 1 # index of first col on display, 1-based not 0-based
        self.history = list() # list of previous commands, earliest first
        self.hindex = 0 # index into history
        self.startup = startup # hooks in to application
        self.cleanup = cleanup
        self.start = start # hooks out to job control
        self.exit = exit
        self.keymap = self.init_keymaps() # define below, minimize clutter here
        # self.state is reassigned only by job control code in another module
        self.state = State.loaded # remain in this state if no job control
        self.yank_buffer = ''  # string from previous ^K kill or ^U discard
        self.yank_enabled = False # might be overridden by multiline yank

    # Piety Session switch method requires job has method named resume
    def resume(self, *args, **kwargs):
        self.startup(*args, **kwargs)
        self.restart()

    def __call__(self, *args, **kwargs):
        self.start()
        self.resume(*args, **kwargs)

    def stop(self):
        self.restore() # calls print() for newline
        self.cleanup()
        self.exit()

    def run(self, *args, **kwargs):
        """
        Console event loop - run a single Console instance as an application.
        For testing only; handler() blocks, can only run one Console at a time.
        """
        self.__call__(*args, **kwargs)
        while not (self.stopped()
                   or self.line in self.job_control_keys):
            self.handler() # blocks in self.reader at each character
        self.stop()

    def handle_key(self, keycode):
        'Call this handle_key as handler when keycode is already available'
        # keycode might be single character or a sequence of characters.
        # Printable keys require special-case handling,
        # because their method takes an additional argument: the key itself.
        if keycode in printing_chars:
            method = self.keymap()[printable]
            method(keycode)
        elif keycode in self.keymap():
            method = self.keymap()[keycode]
            method()
        elif keycode:
            util.putstr(keyboard.bel) # sound indicates no handler
        else:
            pass # incomplete or unrecognized keycode, do nothing

    def handler(self):
        """
        Call this handler when keycode is not yet available, it calls reader.
        To avoid blocking in reader, must only call handler when input is ready
        """
        keycode = self.reader() # returns '' when keycode is not complete
        if keycode:
            self.handle_key(keycode)

    # These keys have job control fcn only if they are alone at start of line.
    # Otherwise they can edit - C_d appears in lineedit_keymap.
    def ctrl_d(self):
        if self.line == '':
            self.line = keyboard.C_d # so job control code can find it
            util.putstr('^D')  # no newline, caller handles it.
            self.stop()
        else:
            self.delete_char()

    def ctrl_z(self):
        if self.line == '':
            self.line = keyboard.C_z # so job control code can find it
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
    # accept_line (when the user finishes entering/editing text in input mode)
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

    # accept_line and accept_command invoke the other methods in this section.
    # These are the methods that are invoked from the keymaps.
    # accept_line is used in insert modes, accept_command in command modes.
    def accept_line(self):
        'For insert modes: handle line, but no history, exit, or job control'
        self.restore()      # advance line and put terminal in line mode 
        self.process_line() # might reassign self.line
        self.restart()      # print prompt and put term in character mode

    def process_command(self):
        'add command to history then execute it'
        self.history.append(self.line)
        self.hindex = len(self.history) - 1
        self.restore()
        self.process_line() # might stop or preempt this job, assign self.state

    def accept_command(self):
        'For command modes: handle line, with history, exit, and job control'
        self.process_command()
        if self.stopped():
            self.stop()
        elif self.state != State.background: #assigned by job control elsewhere
            self.restart()
        else:
            return # a different job continues

    def restart(self):
        'Prepare to collect a line'
        self.line = '' # empty line at beginning of cycle
        self.point = 0 # index into self.line at beginning of cycle
        self.start_col = len(self.prompt())+1 # 1-based indexing, not 0-based
        util.putstr(self.prompt() + self.line) # line might be empty
        self.move_to_point() # might not be end of line
        terminal.set_char_mode()

    # Command history

    def retrieve_previous_history(self):
        if self.history:
            length = len(self.history)
            self.hindex = self.hindex if self.hindex < length else length-1
            self.line = self.history[self.hindex]
            self.point = len(self.line)
            self.start_col = len(self.prompt())+1 # 1-based indexing, not 0
        self.hindex = self.hindex - 1 if self.hindex > 0 else 0

    def retrieve_next_history(self):
        length = len(self.history)
        self.hindex = self.hindex + 1 if self.hindex < length else length
        self.line = (self.history[self.hindex] 
                          if self.hindex < length else '')
        self.point = len(self.line)
        self.start_col = len(self.prompt())+1 # 1-based indexing, not 0

    def previous_history(self):
        self.retrieve_previous_history()
        self.redraw() # tty requires a different method here

    def next_history(self):
        self.retrieve_next_history()
        self.redraw()

    # Editing that requires a display terminal with cursor addressing

    def move_to_point(self):
        # move_to_column and start_col are 1-based but self.point is 0-based
        display.move_to_column(self.start_col + self.point)
 
    def move_beginning(self):
        self.point = 0
        self.move_to_point()

    def move_end(self):
        self.point = len(self.line)
        self.move_to_point()

    def insert_char(self, keycode):
        self.line = (self.line[:self.point] + keycode +
                      self.line[self.point:])
        self.point += 1
        display.insert_char(keycode)

    def backward_delete_char(self):
        if self.point > 0:
            self.line = (self.line[:self.point-1] + 
                            self.line[self.point:])
            self.point -= 1
            display.backward_delete_char()

    def backward_char(self):
        if self.point > 0:
            self.point -= 1
            display.backward_char()

    def delete_char(self):
        self.line = (self.line[:self.point] + self.line[self.point+1:])
        display.delete_char() # point does not change

    def forward_char(self):
        if self.point < len(self.line):
            self.point += 1
            display.forward_char()

    def kill(self):
        '^K, delete line from point to end-of-line'
        self.yank_buffer = self.line[self.point:]
        self.yank_enabled = True
        self.line = self.line[:self.point] # point does not change
        display.kill_line()
        
    def redraw(self):
        'redraw line'
        display.move_to_column(self.start_col)
        self.point = len(self.line)
        util.putstr(self.line)
        display.kill_line() # remove any leftover text past self.line

    def discard(self): # name like gnu readline unix-line-discard
        'discard line'
        self.yank_buffer = self.line
        self.yank_enabled = True
        self.line = str() 
        self.move_beginning() # accounts for prompt, assigns point
        display.kill_line() # erase from cursor to end of line

    def yank(self):
        '^Y, paste line previously ^K killed or ^U discarded'
        self.line = (self.line[:self.point] + self.yank_buffer +
                      self.line[self.point:])
        self.point += len(self.yank_buffer)
        display.insert_string(self.yank_buffer)

    def status(self):
        '^T handler, can override this method with custom handlers in subclasses'
        util.putstr(' '.join(sys.argv)) # just echo the command line for now
        
    def init_keymaps(self):
        """
        Returns a callable with no arguments that returns the keymap
        for handling both commands and input text.  We return a
        callable, not just a keymap, because the needed keymap
        contents might need to be computed because they can depend on
        the application state (mode).  This method returns
        command_keymap defined below (actually it returns lambda:
        command_keymap).  This method also defines several other
        keymaps that the caller can use to construct and assign more
        complex keymap callables.

        A keymap is a dict from a keycode to one of the Console
        methods above.  Keycodes in the keymap can have multiple chars
        (for example esc sequences).

        Keymaps in this class require a video terminal with cursor addressing.
        """
        # This keymap is used in ed (etc.) input mode
        self.input_keymap = {
            # Printable characters require special case in handler method
            #  because their method takes an additional argument: the keycode.
            printable: self.insert_char,

            # any keycode that maps to accept_line exits from line entry/edit
            keyboard.cr: self.accept_line, # but don't add to history
            keyboard.C_c: self.interrupt,

            # line editing
            keyboard.bs: self.backward_delete_char,
            keyboard.delete: self.backward_delete_char,
            keyboard.C_a: self.move_beginning,
            keyboard.C_b: self.backward_char,
            keyboard.C_d: self.delete_char,
            keyboard.C_e: self.move_end,
            keyboard.C_f: self.forward_char,
            keyboard.C_k: self.kill,
            keyboard.C_l: self.redraw,
            keyboard.C_t: self.status,
            keyboard.C_u: self.discard,
            keyboard.C_y: self.yank,

            # These keys are multicharacter control sequences
            # require keyboard that sends ANSI control sequences
            # and keyboard reader that handles multicharacter keycodes
            keyboard.right: self.forward_char,
            keyboard.left: self.backward_char,
            }

        # These keys are active in ed (etc.) command mode. 
        # This command mode keymap requires a video terminal with arrow keys.
        self.command_keys = {
            # Any keycode that maps to accept_command is a command terminator.
            keyboard.cr: self.accept_command, # add to history, possibly exit
            keyboard.C_n: self.next_history,
            keyboard.C_p: self.previous_history,
            keyboard.up: self.previous_history,
            keyboard.down: self.next_history,
        }

        # These keys have job ctrl function only when alone at start of line
        # in cmd mode. Otherwise they can edit - C_d appears in input_keymap.
        self.job_control_keys = {
            keyboard.C_d: self.ctrl_d,
            keyboard.C_z: self.ctrl_z,
            }

        # Combine the keymaps - command mode adds several keys to input mode,
        #  also reassigns method for keyboard.cr (RET key).
        # job_control_keys replaces ^D del in input_keymap with eof 
        #  and adds ^Z suspend.
        # This keymap is the default that __init__ assigns to self.keymap.
        # Be sure to preserve original input_keymap, we use it in input mode
        self.command_keymap = self.input_keymap.copy() # preserve original
        self.command_keymap.update(self.command_keys)
        self.command_keymap.update(self.job_control_keys)

        return (lambda: self.command_keymap) # default keymap
        
def main():
    # Test: echo input lines, use job control commands ^D ^Z to exit.
    echo = Console(prompt=(lambda: '> '), 
                   process_line=(lambda line: print(line)))
    echo.run()

if __name__ == '__main__':
    main()
