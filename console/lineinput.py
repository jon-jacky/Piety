"""
lineinput.py - LineInput class, in-line editing of strings.
           Provides subset of readline editing functions.
           BUT unlike readline, can assign an initial string to edit.
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


# This keymap requires a video terminal with cursor addressing
vt_keymap = {
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
    keyboard.C_l: 'redraw_current_line',
    keyboard.C_u: 'line_discard',

    # These keys are multicharacter control sequences
    # require keyboard that sends ANSI control sequences
    # and keyboard reader that handles multicharacter keycodes
    keyboard.right: 'forward_char',
    keyboard.left: 'backward_char',
    }

class LineInput(object):
    def __init__(self, keymap=vt_keymap):
        self.reinit()
        self.keymap = keymap

    def reinit(self, line='', prompt='', point=None):
        self.line = line
        self.point = point if point != None else len(self.line) # end of line
        self.start_col = len(prompt)+1 # 1-based indexing, not 0-based
        
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

    # Simple command editing that works on printing terminals

    def self_append_command(self, key):
        self.line += key
        self.point += 1
        util.putstr(key)

    def backward_delete_last_char(self):
        if self.point > 0:
            ch = self.line[-1]
            self.line = self.line[:-1]
            self.point -= 1
            # util.putstr('^H') # omit, it is more helpful to echo
            util.putstr('\\%s' % ch) # echo \c where c is deleted char

    # Command editing that requires a display terminal with cursor addressing

    def move_to_point(self):
        display.move_to_column(self.start_col + self.point)
 
    def move_beginning_of_line(self):
        self.point = 0
        self.move_to_point()

    def move_end_of_line(self):
        self.point = len(self.line)
        self.move_to_point()

    def self_insert_command(self, key):
        self.line = (self.line[:self.point] + key +
                      self.line[self.point:])
        self.point += 1
        display.self_insert_char(key)

    def backward_delete_char(self):
        if self.point > 0:
            self.line = (self.line[:self.point-1] + self.line[self.point:])
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

    def kill_line(self):
        self.line = self.line[:self.point] # point does not change
        display.kill_line()

    def redraw_current_line(self):
        # Maybe ^L on vt should refresh whole window or even whole frame?
        display.move_to_column(self.start_col)
        self.point = len(self.line)
        util.putstr(self.line)
        display.kill_line() # remove any leftover text past self.line

    def line_discard(self): # name like gnu readline unix-line-discard
        self.line = str() 
        self.move_beginning_of_line() # accounts for prompt, assigns point
        display.kill_line() # erase from cursor to end of line

# Test - shows how much setup, teardown, event handling lineinput needs

command = LineInput() # outside main() so we can inspect from >>>

def main():
    import terminal # only needed for this test

    def edit():
        'event loop for testing lineinput'
        while True:
            # reads single chars, arrow keys won't work
            key = terminal.getchar()
            if key in printing_chars or key in command.keymap:
                command.handler(key)
            else:
                break

    print('Enter and edit a fresh line:')
    # Typically, caller assigns prompt and start column
    # based on Command restart method
    prompt = '> '
    command.start_col = len(prompt) + 1
    command.line = ''
    command.point = len(command.line)
    util.putstr(prompt)
    terminal.set_char_mode()
    # lineinput event loop
    edit()
    # based on Command restore method
    terminal.set_line_mode()
    print() # advance to next line
    print(command.line) # echo so we can see what we edited

    # Caller can reassign prompt etc. and line to edit
    print('Now edit a previously entered line:')
    prompt = '>> '
    command.start_col = len(prompt) + 1
    command.line = 'Here is some text to edit.'
    command.point = len(command.line)
    util.putstr(prompt)
    util.putstr(command.line) # show line to edit
    terminal.set_char_mode()
    edit()
    terminal.set_line_mode()
    print()
    print(command.line)

if __name__ == '__main__':
    main()
