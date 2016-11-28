"""
inputline.py - InputLine class, entry and editing of single-line strings.
           Provides subset of readline editing functions.
           BUT unlike readline, can assign an initial string to edit.
"""

import string
import display, keyboard, util

# A keymap is a dictionary from keycode string to a method name string.
# Keymap alues are name strings not objects, so they can refer to bound methods.

# Keycodes in keymap can be multicharacter sequences, not just single characters.
# Most method names in the keymap are derived from GNU readline or Emacs,
# but line operand is implicit: redraw-current-line is just redraw here etc.
# Also remove confusing use of 'self', self-insert-char is just insert_char here.
# Retain _char suffix, we might add delete_word, insert_word etc.

printable = 'a' # proxy in keymaps for all printable characters
printing_chars = string.printable[:-5] # exclude \t\n\r\v\f at the end

# This keymap requires a video terminal with cursor addressing
keymap = {
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

# This keymap works on a printing terminal.
tty_keymap = {
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

class InputLine(object):
    def __init__(self, prompt='', line='', point=None, keymap=keymap):
        self.reinit(prompt=prompt, line=line, point=point)
        self.keymap = keymap

    def reinit(self, prompt=None, line=None, point=None):
        self.prompt = self.prompt if prompt is None else prompt
        self.start_col = len(self.prompt)+1 # 1-based indexing, not 0-based
        self.line = self.line if line is None else line
        self.point = len(self.line) if point is None else point
        
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

    # Command editing that requires a display terminal with cursor addressing

    def move_to_point(self):
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

    def kill(self):
        'delete line from point to end-of-line'
        self.line = self.line[:self.point] # point does not change
        display.kill_line()

    def redraw(self):
        'redraw line'
        # Maybe ^L on vt should refresh whole window or even whole frame?
        display.move_to_column(self.start_col)
        self.point = len(self.line)
        util.putstr(self.line)
        display.kill_line() # remove any leftover text past self.line

    def discard(self): # name like gnu readline unix-line-discard
        'discard line'
        self.line = str() 
        self.move_beginning() # accounts for prompt, assigns point
        display.kill_line() # erase from cursor to end of line

    # Command editing that works on printing terminals

    def append_char(self, keycode):
        self.line += keycode
        self.point += 1
        util.putstr(keycode)

    def backward_delete_last_char(self):
        if self.point > 0:
            ch = self.line[-1]
            self.line = self.line[:-1]
            self.point -= 1
            # util.putstr('^H') # omit, it is more helpful to echo
            util.putstr('\\%s' % ch) # echo \c where c is deleted char

    def discard_tty(self): # name like gnu readline unix-line-discard
        'discard entire line including prompt on printing terminal'
        self.line = ''
        util.putstr('^U\r\n' + self.prompt)  # prompt on new line

    def redraw_with_prefix(self, prefix):
        'redraw entire line with prefix and prompt on printing terminal'
        util.putstr(prefix + self.prompt)
        self.redraw()

    def redraw_tty(self):
        'redraw entire line including prompt on printing terminal'
        self.redraw_with_prefix('^L\r\n')

# Test - shows how much setup, teardown, event handling inputline needs

command = InputLine(prompt='> ') # outside main() so we can inspect from >>>

# uncomment this line, comment out the previous, to test TTY mode
#command = InputLine(prompt='> ', keymap=tty_keymap)

def main():
    import terminal # only needed for this test

    def edit():
        'event loop for testing inputline'
        while True:
            # reads single chars, arrow keys won't work
            key = terminal.getchar()
            if key in printing_chars or key in command.keymap:
                command.handler(key)
            else:
                break

    print('Enter and edit a fresh line:')
    util.putstr(command.prompt)
    terminal.set_char_mode()
    # inputline event loop
    edit()
    # based on Console restore method
    terminal.set_line_mode()
    print() # advance to next line
    command.redraw() # echo so we can see what we edited
    print()

    # Caller can reassign prompt, line to edit, and point
    print('Now edit a previously entered line:')
    command.reinit(prompt='>> ', line='Here is some text to edit.', point=0)
    util.putstr(command.prompt)
    # command.redraw() # no good - resets point
    util.putstr(command.line) # preserves point
    command.move_to_point()   # restore cursor to point
    terminal.set_char_mode()
    edit()
    terminal.set_line_mode()
    print()
    print(command.line)

if __name__ == '__main__':
    main()
