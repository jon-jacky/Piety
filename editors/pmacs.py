"""
pmacs.py - Invoke editor functions with emacs keys (control keys or key seqs).

The module name pmacs differs from the editor function name pm
so the function name does not shadow the module name when we do
'from pmacs import pm' so we can type the function name in the REPL
without the module name prefix, just pm() not pmacs.pm().   
Then, if we edit more commands into pm, we can load them without restarting
the session by reload(pmacs).  The argument to reload must be the module name.
"""

import util, terminal, key, edsel
import sked as ed
from keyseq import keyseq

def append():
    'Restore line mode, run edsel a(), return to char mode'
    terminal.set_line_mode()
    edsel.a()
    terminal.set_char_mode()

# Table from keys to editor functions
keycode = {
    key.C_n: edsel.l,  # next line
    key.C_p: edsel.rl,  # previous line
    key.C_v: edsel.v,   # page down
    key.M_v: edsel.rv,  # page up
    key.M_lt: (lambda: edsel.p(1)), # go to top, line 1.  lt is <.
    key.M_gt: (lambda: edsel.p(ed.S())), # go to bottom, last line.  gt is >.
    key.C_k: edsel.d,   # delete line
    key.C_y: edsel.y,   # yank (paste) deleted line
    key.M_q: edsel.wrap,  # wrap, single long line
    key.cr: append,   # open line and enter append mode 
    key.C_l: edsel.refresh, # refresh, frame
    key.C_x + key.C_s : edsel.w  # write file, with stored filename
}

def pm():
    """
    pmacs editor: invoke editor functions with emacs control keys.
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
