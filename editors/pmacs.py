"""
pmacs.py - Invoke editor functions with emacs keys (control keys or key seqs).
"""

import util, terminal, key, edsel
from keyseq import keyseq

keycode = {
    key.C_n: edsel.l,  # next line
    key.C_p: edsel.rl,  # previous line
    key.C_v: edsel.v,   # page down
    key.M_v: edsel.rv  # page up
}

def pmacs():
    """
    Invoke editor functions with emacs keys (control keys or key sequences).
    Supported keys and the fcns they invoke are expressed in keycode table.
    Exit by typing C_z (that's ^Z).
    """
    terminal.set_char_mode()
    while True:
        c = terminal.getchar()
        k = keyseq(c)
        if k: # keyseq returns '' if key sequence is not complete
            if k == key.C_z:
                break
            else:
                fcn = keycode.get(k, lambda: util.putstr(key.bel))
                fcn()
    terminal.set_line_mode()
