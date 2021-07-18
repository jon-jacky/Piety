"""
getkey.py - Get 'key' from keyboard: single character or key sequence

Provides the GetKey class with a __class__ method that gets a'key'
from keyboard: a single character or key sequence.

This method does *not* block after receiving a prefix character  such
as C_x.  Instead, this method  always returns immediately after
receiving each single character.  If the character is a prefix, and
more characters are expected, this method just returns the empty
string, ''.   If the character is not a prefix (it is a printing
character or a self-contained  control character) this method
returns that character.  If the character is the last character in a
multicharacter sequence, this method returns the whole sequence
including the prefix  character(s) and the last character.

Also, the method might read multiple characters in one call,
if more than one character arrived since the last call.  This
might happen for special function keys, arrow keys etc. that include
a prefix plus contents, all sent rapidly.   If the method reads
more than a single character in one call, it immediately returns
the entire sequence of characters it read.

This is implemented by a Python class, not a function, so each instance
can store the prefix character(s) between calls.  The method is a 
__class__ method so it can be called with the same syntax as a function,
as if the instance name were a function name, to make the calls a little
more compact.

Each key sequence begins with prefix character or characters indicating more
follows. ESC is the prefix for the meta commands and terminal control
codes. C_x is the prefix for some key sequences such as C_x o, the
edsel  command  to switch to the other window.  ESC-[ (called CSI) is
the prefix for terminal control codes.

To avoid waiting indefinitely for a sequence that never finishes,
reading C_g (that is, CTRL g or ^g) at any time ends waiting,
discards any incomplete sequence, and immediately returns just C_g.
So the user can type C_g if a program appears hung when reading a command.
C_g is used as the Cancel command by some programs.
"""

import util, terminal, key

class GetKey:

    def __init__(self):
        self.prefix = '' 

    def __call__(self):
    
        c = terminal.getchar() 

        # C_g is the unconditional cancel command, 
        # always discard any prefix and just return C_g itself.
        if c == key.C_g:
            self.prefix = ''
            return key.C_g
    
        # No prefix, prefix character arrives, start prefix
        if self.prefix == '' and c in (key.esc, key.C_x): # more to come?
            self.prefix = c
            return ''
    
        # No prefix, ordinary character arrives, just return this character
        elif self.prefix == '':
            return c

        # Handle each prefix
    
        # esc prefix for meta keys and ANSI terminal control codes
        elif self.prefix == key.esc: 

            # ANSI escape codes for terminal control, begin with esc-[ called csi
            if c == '[':
                self.prefix += '['
                return '' # now keyseq == key.csi, wait for rest of sequence
    
            # Meta keys, begin with esc then one other key but not [
            else:
                keyseq = self.prefix + c
                self.prefix = '' 
                return keyseq

        # CSI prefix for control keys
        elif self.prefix == key.csi:
            # For now we only support the four arrow keys: csi+'A' etc.
            #  with just one char after csi, so we can return now
            keyseq = self.prefix + c
            self.prefix = ''
            return keyseq
    
        # ctrl-X prefix for window commands and buffer commands
        elif self.prefix == key.C_x:
    
            # C_x + one more key
            keyseq = self.prefix + c
            self.prefix = ''
            return keyseq

        # Unrecognized prefix - clear prefix and return this character
        else:
            self.prefix = ''
            return c

def main():
    'Demonstrate getkey'
    getkey = GetKey()

    util.putstr('> ')
    terminal.set_char_mode()
    line = []
    k = 'x' # anything but cr or ''
    while k != key.cr:
        k = getkey() # return '' if incomplete prefix
        line += [k]  # include [''] if incomplete prefix
        util.putstr(k)
    terminal.set_line_mode()
    print() 
    print([ [c for c in k] for k in line ]) # show any esc or other unprintables

if __name__ == '__main__':
    main()

