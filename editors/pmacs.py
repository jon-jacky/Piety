"""
pmacs.py - display editor that uses emacs control keys.

pmacs might mean 'Python emacs' but actually means 'poor emacs'
or 'pathetic emacs' or maybe 'Passing grade emacs, just above Fail'.
"""

import editline, dmacs

def pmcmd(k):
    """
    Execute a single pmacs command
    """
    # FIXME! This refers to dmacs or editline module vars without qualification
    global prev_fcn
    fcn = keymap.get(k, lambda: util.putstr(key.bel))
    fcn()
    prev_fcn = fcn
def pm():
    """
    pmacs editor: invoke editor functions with emacs control keys.
    Exit by typing M_x (that's alt X), like emacs 'do command'.
    """
    global prev_fcn
    open_promptline()
    terminal.set_char_mode()
    while True:
        c = terminal.getchar()
        k = keyseq.keyseq(c)
        if k: # keyseq returns '' if key sequence is not complete
            if k == key.M_x:
                prev_fcn = None # there is no 'exit pmacs' fcn - just do it
                break
            else:
                pm(k)
    close_promptline()
    display.put_cursor(edsel.tlines, 1) # return cursor to command line
    terminal.set_line_mode()
