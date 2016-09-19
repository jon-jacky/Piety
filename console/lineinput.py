"""
lineinput.py - LineInput class, in-line editing of strings.
           Provides subset of readline editing functions.
           BUT unlike readline, can pass in a string to edit.
"""

import string
import display, keyboard, util

# A keymap is a dictionary from keycode string to Command method name string.
# Values are name strings not function objects, so they can refer to bound methods.
# Keycodes in keymap can be multicharacter sequences, not just single characters.
# Most method names in the keymap are the same as in GNU readline or Emacs.

printable = 'a' # proxy in keymaps for all printable characters
printing_chars = string.printable[:-5] # exclude \t\n\r\v\f at the end

# This keymap works on a printing terminal.
printing_keymap = {
    # self_append_command requires special-case handling
    #  because it takes an additional argument: the key.
    printable: 'self_append_command',

    keyboard.C_j: 'newline',
    keyboard.C_l: 'redraw_current_line',
    keyboard.C_u: 'line_discard',

    # Rudimentary in-line editing, just delete last char in line
    keyboard.bs: 'backward_delete_last_char',
    keyboard.delete: 'backward_delete_last_char'
}

editing_keys = {
    # self_insert_command requires special-case handling
    #  because it takes an additional argument: the key.
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
    }

editing_keymap = printing_keymap.copy()
editing_keymap.update(editing_keys)

class LineInput(object):
    def __init__(self, keymap=editing_keymap):
        self.chars = ''  # string to edit
        self.start_col = 1   # column number of left margin, 1-based
        self.point = 0  # index of insertion point in self.chars, 0-based
        self.keymap = keymap
        self.prompt = ''

    # Simple command editing that works on printing terminals
    def handler(self, keycode):
        'Look up command for keycode and run it'
        # keycode arg might be single character or a sequence of characters.
        # Printable keys require special-case handling,
        #  because their method takes an additional argument: the key itself.
        if keycode in printing_chars:
            method = getattr(self, self.keymap[printable])
            method(keycode)
        elif keycode in self.keymap:
            method = getattr(self, self.keymap[keycode])
            method()
        else:
            pass # caller should ensure we never get here

    def self_append_command(self, key):
        self.chars += key
        self.point += 1
        util.putstr(key)

    def backward_delete_last_char(self):
        if self.point > 0:
            ch = self.chars[-1]
            self.chars = self.chars[:-1]
            self.point -= 1
            # util.putstr('^H') # omit, it is more helpful to echo
            util.putstr('\\%s' % ch) # echo \c where c is deleted char

    def redraw_current_line(self):
        util.putstr('^L\r\n' + self.prompt)  # on new line
        #putlines(self.chars) # might be multiple lines
        util.putstr(self.chars)

    def line_discard(self): # name like gnu readline unix-line-discard
        self.chars = str() 
        self.point = 0
        util.putstr('^U\r\n' + self.prompt)

    def newline(self):
        self.chars += '\n'
        self.point += 1
        util.putstr('^J\r\n' + self.continuation)

    # Command editing that requires a display terminal with cursor addressing
 
    def self_insert_command(self, key):
        self.chars = (self.chars[:self.point] + key + \
                        self.chars[self.point:])
        self.point += 1
        display.self_insert_char(key)

    def backward_delete_char(self):
        if self.point > 0:
            self.chars = (self.chars[:self.point-1] + self.chars[self.point:])
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
        self.chars = (self.chars[:self.point] + self.chars[self.point+1:])
        display.delete_char()

    def move_end_of_line(self):
        self.point = len(self.chars)
        eol = len(self.prompt) + 1 + len(self.chars)
        display.move_to_column(eol)

    def forward_char(self):
        if self.point < len(self.chars):
            self.point += 1
            display.forward_char()

    def kill_line(self):
         self.chars = self.chars[:self.point] # point doesn't change
         display.kill_line()

# no test code in this module - useful test must import command, key

