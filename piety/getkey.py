"""
getkey.py - collect single-charactor or multiple-character key sequences
"""

import terminal
import vt_keyboard as keyboard

# FIXME we actually want to update a key (sequence)
# then call a given function when the key sequence is complete

def getkey(char):
    key = char
    if key == keyboard.esc:
        c1 = terminal.getchar()
        if c1 != '[':
            return key # discard esc c1, not ansi ctl seq introducer (csi).
        else:
            key += c1
            c2 = terminal.getchar()
            if c2 not in 'ABCD':  # four arrow keys are esc[A etc.
                return key # discard esc [ c2, not one of the 4 arrow keys
            else:
                key += c2 
                # print ('key: %s' % [c for c in key]) # DEBUG
                # arrow key detected, one of ansi.cuf1 etc.

    return key
