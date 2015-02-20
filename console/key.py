"""
key.py - Collect, store, return single character or multi-character key sequences
          Might specialize (for example) for emacs key seqences: M-x etc.
          This is a class not a just a function because we need 
            an object with local memory: the incomplete key sequence
         (Seems heavyweight for what it does - could we use a generator instead?)
        Has a main method, python key.py demonstrates most functions.
"""

import terminal, keyboard

class Key(object): 
    """
    Collect, store, handle single key or multi-character key sequences.
    Deal with prefixes: esc-[  M-x  C-c etc.
    """
    def __init__(self):
        """
        key - single character or character sequence that comprises a key
        """
        self.key = ''

    def __call__(self):
        """
        Get char from terminal, add to key sequence, check for complete sequence
        Return after each character.  If key sequence not complete, return ''
        If key sequence is complete, return the entire sequence

        CORRECTION: This version does *not* return after each char,
        it collects the entire key sequence and then returns.
        This version never returns ''.

        This version *blocks* while collecting multi-char sequences.
        Should be okay if multi-char sequences come from keyboard,
        but *not* okay for collecting emacs-style commands: M-x ... etc.

        This version *only* handles single character keys, and
        ANSI terminal codes of the form: csi + one character,
        like arrow keys: up esc[A, down esc[B, right esc[C, left esc[D

        This version stops collecting characters and returns sequence
        as soon as key sequence matches esc[c (for any c) 
        or prefix *fails* to match.  

        The handler must deal with unrecognized keys,
        including incomplete prefix sequences.
        """
        # To avoid blocking here, call when select (or...) says char is ready
        # We find that unfortunately select does *not* indicate when
        #  subsequent chars from keyboard key sequences are ready,
        #   so we read them here without returning.
        self.key += terminal.getchar()
        if self.key[-1] == keyboard.esc: # begin escape sequence
            self.key += terminal.getchar() # block waiting for next key
            if self.key[-1] == '[': # esc-[ is ansi ctrl seq introducer, csi
                self.key += terminal.getchar() # block waiting for next key
        # Here we have ansi controll sequence with one char: up esc[A etc.
        k = self.key 
        self.key = ''
        return k 

def main():
    'Demonstrate Key class'
    key = Key()
    print '> ',
    terminal.set_char_mode()
    line = ''
    k = '' # anything but cr
    while k != keyboard.cr:
        k = key()
        line += k
        terminal.putstr(k)
    terminal.set_line_mode()
    print 
    print [ c for c in line ] # show any esc or other unprintables

if __name__ == '__main__':
    main()
