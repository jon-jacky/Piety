"""
pmacs.py - display editor that uses emacs control keys.

pmacs might mean 'Python emacs' but actually means 'poor emacs'
or 'pathetic emacs' or maybe 'Passing grade emacs, just above Fail'.
"""

import terminal, key, keyseq, display, edsel, dmacs
import sked as ed, editline as el

# Define and initialize global variables used by pmacs functions.
# Conditinally exec only the *first* time this module is imported in a session.
# Then we can reload this module without re-initializing those variables.
try:
    _ = saved_put_marker # if already defined, then pmacsinit was already exec
except:
    from pmacsinit import *

# helper functions

def reset_point():
    'Possibly move el.point if needed when dot moves to another line'
    linelen = len(ed.buffer[ed.dot])
    if el.point > linelen:
        el.point = linelen - 1 # -1 to put point before final \n

def restore_cursor_to_window():
    reset_point()
    # point+1 to make put_cursor call consistent with editline move_to_column
    display.put_cursor(edsel.wline(ed.dot), el.point + 1)

# Some functions do not use keycode arg but runcmd and pm require it to be there

def open_line(keycode):
    """
    Split line at point, replace line in buffer at dot
    with its prefix, append suffix after line at dot.
    """
    suffix = ed.buffer[ed.dot][el.point:] # including final \n
    # Keep prefix on dot.  Calls el.kill_line, thanks to key.C_k, not keycode
    ed.buffer[ed.dot] = el.runcmd(key.C_k, ed.buffer[ed.dot]) # prefix on dot
    ed.buffer[ed.dot+1:ed.dot+1] = [ suffix ] # insert suffix line after dot
    ed.dot = ed.dot + 1
    if edsel.in_window(ed.dot):
        edsel.update_below(ed.dot)
    else:
        edsel.recenter()
    el.point = 0 # start of new suffix line
    restore_cursor_to_window()

# The following functions supercede and wrap functions in other modules

def join_prev():
    'Join this line to previous. At first line do nothing.'
    if ed.dot > 1:
        el.point = len(ed.buffer[ed.dot-1])-1 # don't count \n
        edsel.j(ed.dot-1, ed.dot) # defaults in ed.j join dot to dot+1

def delete_backward_char(keycode):
    """
    If point is not at start of line, delete preceding character.
    Otherwise join to previous line.  At start of first line do nothing.
    """
    if el.point > 0:
        # Calls el.delete_backward_char, thanks to keycode DEL key.bs
        ed.buffer[ed.dot] = el.runcmd(keycode, ed.buffer[ed.dot]) 
    else: 
        join_prev() # see above
        restore_cursor_to_window()

def join_next():
    'Join next line to this one. At last line do nothing.'
    if ed.dot < ed.S():
        edsel.j() # defaults in ed.j join dot to dot+1

def delete_char(keycode):
    """
    If point is not at end of line, delete character under cursor.
    Otherwise join next line to this one.  At end of last line do nothing.
    """
    if el.point < len(ed.buffer[ed.dot].rstrip('\n')):
        # Calls el.delete_char, thanks to keycode C_d
        ed.buffer[ed.dot] = el.runcmd(keycode, ed.buffer[ed.dot])
    else:
        join_next() # see above
        restore_cursor_to_window()

def kill_line(keycode):
    """
    In inline mode, kill line from the cursor up to but not including final \n
     save killed segment in editline.killed buffer for subsequent yank.
    In multline mode, kill entire line including final \n
     save consecutive killed lines in sked.killed buffer for subsequent yank.
    Manage transitions between inline and multiline modes:
    kill line on empty line consisting only of \n enters multiline mode.
    kill line after any other command than kill line resumes inline mode.
    """
    global inline
    # Lone kill line or first kill line in a series is inline ...
    if dmacs.prev_cmd != kill_line:
        inline = True
    # ... except begin multiline mode when kill empty line of only \n
    if ed.buffer[ed.dot] == '\n':
        inline = False # Enter multiline mode
        # If this is second consecutive C_k, copy previously killed line from 
        #  inline editline.killed buffer to multiline sked.killed buffer
        if dmacs.prev_cmd == kill_line:
            ed.killed = [el.killed+'\n'] # cp el.killed to 1st line sked.killed
        else: # we just killed empty line of only \n
            ed.killed = [] # clear sked.killed
        el.killed = '' # clear el.killed, start over. NB string not list
        # Delete the empty killed line from the buffer ...
        edsel.d(None,None,True) # ... and append line to killed buffer
        restore_cursor_to_window()
        # Now buffer and display are right, but killed has extra \n line at end
        ed.killed.remove('\n') # remove '\n' line
    # inline kill line:
    elif inline: # weaker condition, must follow previous stronger if...
        ed.buffer[ed.dot] = el.runcmd(keycode, ed.buffer[ed.dot]) # keycode C_k
    # kill line that is part of a multiline sequence:
    elif not inline:
        edsel.d(None,None,True) # consecutive C_k, append line to killed buffer
        restore_cursor_to_window()

def kill_region(keycode):
    global inline
    inline = False
    dmacs.runcmd(keycode) # keycode is C_w here
    restore_cursor_to_window()

def yank(keycode):
    """
    Yank entire line(s) or yank word(s) within a line, depending on inline
    """
    if inline:
        ed.buffer[ed.dot] = el.runcmd(keycode, ed.buffer[ed.dot]) #C_k, el.yank
    else:
        dmacs.runcmd(keycode) # keycode is C_y here
        restore_cursor_to_window()

def refresh(keycode):
    'Define pmacs whole window refresh here so we dont use editline refresh'
    dmacs.runcmd(keycode) # keycode is C_l here
    restore_cursor_to_window() 

def append(keycode):
    dmacs.runcmd(key.cr) # calls dmacs append, which enters append mode.
    restore_cursor_to_window()

keymap = {
    key.cr: open_line, 
    key.delete: delete_backward_char,
    key.bs: delete_backward_char, 
    key.C_d: delete_char,
    key.C_k: kill_line,
    key.C_w: kill_region,
    key.C_y: yank,
    key.C_l: refresh,
    key.C_x + key.C_a: append, # Enter dmacs append mode, exit with .
}

def runcmd(keycode):
    """
    Execute a single pmacs command: dispatch on key k, run function
    """
    cmd = keymap[keycode]
    cmd(keycode)
    dmacs.prev_cmd = cmd
    # FIXME?  A few cmd call el.runcmd but don't update el.prev_cmd first

def clear_marker():
    edsel.put_marker(ed.dot, display.clear)
    display.put_cursor(edsel.tlines, 1)

def put_no_marker(bufline, attribs): 
    'Assign to edsel.put_marker to suppress marker while running pmacs'
    pass

# saved_put_marker is initialized in pmacsinit.py so we can restore

def pm():
    """
    pmacs editor: invoke editor functions with emacs control keys.
    Exit by typing M_x (that's alt X), like emacs 'do command'.
    """
    global inline
    dmacs.open_promptline()
    terminal.set_char_mode()
    clear_marker()
    edsel.put_marker = put_no_marker
    restore_cursor_to_window()
    while True:
        c = terminal.getchar()
        k = keyseq.keyseq(c)
        if k: # keyseq returns '' if key sequence is not complete
            if k == key.M_x:
                break
            elif k in keymap:
                runcmd(k)
            elif k in el.printing_chars or k in el.keymap:
                el.prev_cmd = dmacs.prev_cmd
                ed.buffer[ed.dot] = el.runcmd(k, ed.buffer[ed.dot])
                dmacs.prev_cmd = el.prev_cmd
                if k in (key.M_d, key.C_u): # M_d kill_word, C_u discard line 
                    inline = True
            elif k in dmacs.keymap:
                edsel.restore_cursor_to_cmdline()
                dmacs.runcmd(k)
                restore_cursor_to_window()
    dmacs.close_promptline()
    edsel.put_marker = saved_put_marker # initialized in pmacsinit.py
    edsel.put_marker(ed.dot, display.white_bg)
    edsel.restore_cursor_to_cmdline()
    terminal.set_line_mode()
