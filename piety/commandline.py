"""
commandline.py - skeleton command line application for Piety
"""

import sys
import string

# These imports hide platform dependencies.
import terminal
# For vt100-style terminal with ansi escape sequences, arrow keys.
# Replace these two imports to use a different keyboard and display.
import vt_keyboard as keyboard
import vt_display as display

# Print regrets when ^D but no self.exit
noexit = 'No exit function defined, type ^C for KeyboardInterrupt'

def echoline(cmdline):
    'Print cmdline on console'
    print cmdline

class Console(object):
    """
    Skeleton command line application for Piety.  Has a getchar method
    that gets a key typed at the console and adds it to a command
    line (usually).  

    Schedule getchar from the Piety scheduler for non-blocking command
    input.  When getchar gets a line terminator character, it calls a
    command function and passes the command line to it.  

    The 'key' might actually be a multi-character control sequence (as
    in Emacs).  Some of the keys do command line editing.
    """
    def __init__(self, prompt='> ', command=None, exiter=exit):
        """
        prompt - optional argument, prompt string, default is 'piety>'
        command - optional argument, function to execute command line,
          can be any callable that takes one argument, a string.
          Default just echoes the command line.
        exiter - optional argument, function to call in response to ^D key.
          default merely prints a line advising ^C to interrupt.
        """
        self.cmdline = str()
        self.point = 0 # index where next character will be inserted
        self.prompt = prompt
        self.command = command if command else echoline # fcn to call
        # the parameter is named exiter to avoid clash with built-in exit
        # self.exit is okay because it is not ambiguous
        self.exit = exiter # function to call to exit
        self.history = list() # list of cmdline, earliest first
        self.iline = 0 # index into cmdline history
        self.continuation = '.'*(len(self.prompt)-1) + ' ' # prompt

        # associate keys with commands (methods)
        # edit here or reassign later to change key assignments
        # command names are from emacs or gnu readline 
        self.keymap = { 
            # command line management
            keyboard.cr: self.accept_line,
            keyboard.C_l: self.redraw_current_line,
            keyboard.C_u: self.line_discard,
            keyboard.C_j: self.newline,
            keyboard.C_p: self.previous_history,
            keyboard.up: self.previous_history,
            keyboard.C_n: self.next_history,
            keyboard.down: self.next_history,
            keyboard.C_c: self.interrupt,
            # line editing
            keyboard.bs: self.backward_delete_char,
            keyboard.delete: self.backward_delete_char,
            keyboard.C_a: self.move_beginning_of_line,
            keyboard.C_b: self.backward_char,
            keyboard.left: self.backward_char,
            keyboard.C_e: self.move_end_of_line,
            keyboard.C_f: self.forward_char,
            keyboard.right: self.forward_char,
            keyboard.C_k: self.kill_line,
            # keys used in both modes
            keyboard.C_d: self.handle_C_d,
            # printable characters: self.self_insert_command, below
            }

        if key in self.keymap:
            self.keymap[key]()
        elif key in string.printable:
            self.self_insert_command(key)
        else:
            print keyboard.bel, # sound indicates key not handled
        return key # caller might check for 'q' quit cmd or ...
