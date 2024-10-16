"""
keyseq_1.py - construct emacs-style key sequence from one or more characters.
              This is the old version that does not work in the asyncio loop.
              Compare to the new keyseq.py.             
"""

import terminal, key

prefix = '' #  incomplete key sequence

def keyseq(c):
    """
    Construct emacs-style key sequence from one or more characters.
    On each call, pass in a single character.
    Do not block waiting for sequence to complete, return after each call.
    When sequence is complete, return the entire sequence (maybe single char).
    When sequence is incomplete, return the empty string ''.
    Pass in C_g (^G) to cancel incomplete sequence and just return C_g.
    """
    global prefix

    # C_g is the unconditional cancel command, 
    # always discard any prefix and just return C_g itself.
    if c == key.C_g:
        prefix = ''
        return key.C_g

    # No prefix, prefix character arrives, start prefix
    if prefix == '' and c in (key.esc, key.C_x, key.C_c): # more to come?
        prefix = c
        return ''

    # No prefix, ordinary character arrives, just return this character
    elif prefix == '':
        return c

    # Handle each prefix

    # esc prefix for meta keys and ANSI terminal control codes
    elif prefix == key.esc: 
        # ANSI escape codes for terminal control, begin with esc-[ called csi
        if c == '[':
            prefix += '['
            return '' # now prefix == key.csi, wait for rest of sequence

        # Meta keys, begin with esc then one other key but not [
        else:
            kseq = prefix + c
            prefix = '' 
            return kseq

    # CSI prefix for control keys
    elif prefix == key.csi:
        # For now we only support the four arrow keys: csi+'A' etc.
        #  with just one char after csi, so we can return now
        kseq = prefix + c
        prefix = ''
        return kseq

    # ctrl-X prefix for window commands and buffer commands
    elif prefix == key.C_x:
        # C_x + one more key
        kseq = prefix + c
        prefix = ''
        return kseq

    # ctrl-C prefix for indent commands
    elif prefix == key.C_c:
        # C_c + one more key
        kseq = prefix + c
        prefix = ''
        return kseq

    # Unrecognized prefix - clear prefix and return this character
    else:
        prefix = ''
        return c

def main():
    'Demonstrate keyseq'
    terminal.putstr('> ')
    terminal.set_char_mode()
    line = []
    k = 'x' # anything but cr or ''
    while k != key.cr:
        c = terminal.getchar()
        k = keyseq(c) # return '' if incomplete prefix
        line += [k]  # include [''] if incomplete prefix
        terminal.putstr(k)
    terminal.set_line_mode()
    print() 
    print([ [c for c in k] for k in line ]) # show any esc or other unprintables

if __name__ == '__main__':
    main()

