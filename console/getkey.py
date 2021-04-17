"""
getkey.py - Get 'key' from keyboard: single character or key sequence
"""

import util, terminal, key

def getkey():
    """
    Get 'key' from keyboard: single character or key sequence.
        
    This version *blocks* while collecting multi-character key sequences.
    We find that unfortunately select does *not* indicate when
    subsequent chars from keyboard key sequences are ready,
    so we read each character from here without returning.

    Each key sequence begins with prefix char or chars indicating more follows.
    esc is the prefix for the meta commands and terminal control codes.
    esc-[ (called csi) is the prefix for terminal control codes.

    To avoid blocking indefinitely waiting for a sequence that never finishes,
    reading C_g (that is, CTRL g or ^g) at any time ends waiting,
    discards any incomplete sequence, and immediately returns just C_g.
    So the user can type C_g if a program appears hung when reading a command.
    C_g is used as the Cancel command by some programs.
    """
    keyseq = terminal.getchar()

    # Handle each prefix as a special case

    # esc prefix for meta keys and ANSI terminal control codes
    if keyseq == key.esc: 
        keyseq += terminal.getchar() # block waiting, then get next key

        # C_g is the cancel command, stop waiting for more keys and return now
        if keyseq[-1] == key.C_g:
            return key.C_g

        # ANSI escape codes for terminal control, begin with esc-[ called csi
        elif keyseq == key.csi:
            keyseq += terminal.getchar() # block waiting, then get next key
            # For now we only support the four arrow keys: csi+'A' etc.
            #  with just one char after csi, so we can return now
            return keyseq

        # Meta keys, begin with esc then one other key but not [
        else:
            return keyseq

    # ctrl-X prefix for window commands and buffer commands
    elif keyseq == key.C_x:
        keyseq += terminal.getchar() # block waiting, then get next key

        # C_g is the cancel command, stop waiting for more keys and return now
        if keyseq[-1] == key.C_g:
            return key.C_g

        # C-x M-<char> just returns  M-<char>
        # FIXME? This code doesn't handle C-g or ANSI escape sequences
        elif keyseq[-1] == key.esc:
            keyseq += terminal.getchar() # get <char> after esc
            return keyseq[-2:] # return M-<char>

        # C_x + one more key
        else:
            return keyseq

    # Other prefixes to come? Maybe C-c and the whole Emacs menagerie

    # No prefix - just return the single character
    else:
        return keyseq

def main():
    'Demonstrate getkey function'
    util.putstr('> ')
    terminal.set_char_mode()
    line = ''
    k = '' # anything but cr
    while k != key.cr:
        k = getkey()
        line += k
        util.putstr(k)
    terminal.set_line_mode()
    print() 
    print([ c for c in line ]) # show any esc or other unprintables

if __name__ == '__main__':
    main()

