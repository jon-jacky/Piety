"""
key.py - Collect, store, handle single key or multi-character key sequences

Has a main method, python key.py demonstrates most functions.
"""

import terminal
import vt_keyboard as keyboard

class Key(object): 
    """
    Collect, store, handle single key or multi-character key sequences.
    Deal with prefixes: esc-[  M-x  C-c etc.
    When key sequence is complete, call a handler 
    """
    def __init__(self, handler):
        """
        key - single character or character sequence that comprises a key
        handler - function to call when key is complete
        """
        self.key = ''
        self.handler = handler

    def getchar(self):
        """
        Get character from terminal, add to key sequence,
        call handler when sequence is complete.

        Currently this does *not* return after each char,
        it collects the entire key sequence and then calls the handler.
        So this *blocks* while collecting multi-char sequences.
        Should be okay if multi-char sequences come from keyboard,
        but *not* okay for collecting emacs-style commands: M-x ... etc.

        Currently this *only* handles single characters, and
        ANSI terminal codes of the form: csi + one character,
        like arrow keys: up esc[A, down esc[B, right esc[C, left esc[D

        This stops collecting characters and calls handler
        as soon as key sequence matches esc[c (for any c) 
        or prefix *fails* to match.  

        The handler must deal with unrecognized keys,
        including incomplete prefix sequences.
        """
        # To avoid blocking here, call when select (or..) says char is ready
        # We find that unfortunately select does *not* indicate when
        #  subsequent chars from keyboard key sequences are ready,
        #   so we read them here without returning.
        self.key += terminal.getchar()
        if self.key[-1] == keyboard.esc: # begin escape sequence
            self.key += terminal.getchar() # block waiting for next key
            if self.key[-1] == '[': # esc-[ is ansi ctrl seq introducer, csi
                self.key += terminal.getchar() # block waiting for next key
        # Here we have ansi controll sequence with one char: up esc[A etc.
        self.handler(self.key)
        k = self.key 
        self.key = ''
        return k 

# Test

def handler(key):
    'Just output the character to the terminal'
    terminal.putstr(key)

def main():
    'Demonstrate Key class and its getchar method'
    k = Key(handler)
    print '> ',
    terminal.set_char_mode()
    line = ''
    key = '' # anything but cr
    while key != keyboard.cr:
        key = k.getchar()
        line += key
    terminal.set_line_mode()
    print 
    print [ c for c in line ] # show any esc or other unprintables

if __name__ == '__main__':
    main()
