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
    # and keyboard reader that handles multicharacter keycodes
    keyboard.right: 'forward_char',
    keyboard.left: 'backward_char',
    }

editing_keymap = printing_keymap.copy()
editing_keymap.update(editing_keys)

class LineInput(object):
    def __init__(self, keymap=editing_keymap):
        self.chars = '' # string to edit
        self.point = 0  # index of insertion point in self.chars, 0-based
        self.start = 1  # index of first column on display, 1-based
        self.keymap = keymap
        
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

    # Command editing that requires a display terminal with cursor addressing
 
    def self_insert_command(self, key):
        self.chars = (self.chars[:self.point] + key +
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
        display.move_to_column(self.start)

    def backward_char(self):
        if self.point > 0:
            self.point -= 1
            display.backward_char()

    def delete_char(self):
        self.chars = (self.chars[:self.point] + self.chars[self.point+1:])
        display.delete_char()

    def move_end_of_line(self):
        self.point = len(self.chars)
        eol = self.start + len(self.chars)
        display.move_to_column(eol)

    def forward_char(self):
        if self.point < len(self.chars):
            self.point += 1
            display.forward_char()

    def kill_line(self):
         self.chars = self.chars[:self.point] # point doesn't change
         display.kill_line()

# Test - shows how much setup, teardown, event handling lineinput needs

line = LineInput() # outside main() so we can inspect from >>>

def main():
    import terminal # only needed for this test

    def edit():
        'event loop for testing lineinput'
        while True:
            # reads single chars, arrow keys won't work
            key = terminal.getchar()
            if key in printing_chars or key in line.keymap:
                line.handler(key)
            else:
                break

    print('Enter and edit a fresh line:')
    # Typically, caller assigns prompt and start column
    # based on Command restart method
    prompt = '> '
    line.chars = ''
    line.start = len(prompt) + 1
    util.putstr(prompt)
    terminal.set_char_mode()
    # lineinput event loop
    edit()
    # based on Command restore method
    terminal.set_line_mode()
    print()

    # Caller can reassign prompt etc. and line to edit
    print('Now edit a previously entered line:')
    prompt = '>> '
    line.chars = 'Here is some text to edit.'
    line.start = len(prompt) + 1
    util.putstr(prompt)
    util.putstr(line.chars) # show line to edit
    terminal.set_char_mode()
    edit()
    terminal.set_line_mode()
    print()

if __name__ == '__main__':
    main()
