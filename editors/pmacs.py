"""
pmacs.py - display editor that uses emacs control keys.

pmacs might mean 'Python emacs' but actually means 'partly inspired by emacs'
or maybe 'poor imitation of emacs'.
"""

import terminal, key, keyseq, display, edsel, dmacs
import sked as ed, editline as el

# Define and initialize global variables used by pmacs functions,
# but only the *first* time this module is imported in a session.
# Then we can reload this module without re-initializing those variables.
try:
    _ = saved_put_marker # if already defined, then pmacs was already imported
except:
    inline = True # kill (cut) and yank (paste) within a single line
    start_col = 0  # default 0, no prompt or etc. at left margin
    saved_put_marker = edsel.put_marker # so we can restore after put_no_marker

# helper functions

def reset_point():
    'Possibly move ed.point if needed when dot moves to another line'
    linelen = len(ed.buffer[ed.dot])
    if ed.point > linelen:
        ed.point = linelen - 1 # -1 to put point before final \n

def restore_cursor_to_window():
    # reset_point() # no longer needed here, each pmacs fcn maintains ed.point
    # point+1 to make put_cursor call consistent with editline move_to_column
    display.put_cursor(edsel.wline(ed.dot), ed.point + 1)

# Some functions do not use keycode arg but runcmd and pm require it to be there

def next_line(keycode):
    'Move to next line, same column, or end of line if next line is too short'
    edsel.l() # advances dot
    reset_point() # move to end of line if next line is too short
    restore_cursor_to_window()

def prev_line(keycode):
    'Move to previous line, same col, or end of line if prev line is too short'
    edsel.rl() # decrements dot
    reset_point() # move to end of line if previous line is too short
    restore_cursor_to_window()

def open_line(keycode):
    """
    Split line at point, replace line in buffer at dot
    with its prefix, append suffix after line at dot.
    """
    suffix = ed.buffer[ed.dot][ed.point:] # including final \n
    # Keep prefix on dot.  Calls el.kill_line, thanks to key.C_k, not keycode
    ed.buffer[ed.dot], ed.point = el.runcmd(key.C_k, ed.buffer[ed.dot],
                                             ed.point, start_col)
    ed.buffer[ed.dot+1:ed.dot+1] = [ suffix ] # insert suffix line after dot
    ed.dot = ed.dot + 1
    if edsel.in_window(ed.dot):
        edsel.update_below(ed.dot)
    else:
        edsel.recenter()
    ed.point = 0 # start of new suffix line
    restore_cursor_to_window()

# The following functions supercede and wrap functions in other modules

def join_prev():
    'Join this line to previous. At first line do nothing.'
    if ed.dot > 1:
        ed.point = len(ed.buffer[ed.dot-1])-1 # don't count \n
        edsel.j(ed.dot-1, ed.dot) # defaults in ed.j join dot to dot+1

def delete_backward_char(keycode):
    """
    If point is not at start of line, delete preceding character.
    Otherwise join to previous line.  At start of first line do nothing.
    """
    if ed.point > 0:
        # Calls el.delete_backward_char, thanks to keycode DEL key.bs
        ed.buffer[ed.dot], ed.point = el.runcmd(keycode, ed.buffer[ed.dot],
                                                ed.point, start_col) 
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
    if ed.point < len(ed.buffer[ed.dot].rstrip('\n')):
        # Calls el.delete_char, thanks to keycode C_d
        ed.buffer[ed.dot], ed.point = el.runcmd(keycode, ed.buffer[ed.dot],
                                                ed.point, start_col)
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
    #      and we are not already in multiline mode
    if ed.buffer[ed.dot] == '\n' and inline: 
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
        ed.buffer[ed.dot], ed.point = el.runcmd(keycode, ed.buffer[ed.dot],
                                                ed.point, start_col)
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
        ed.buffer[ed.dot], ed.point = el.runcmd(keycode, ed.buffer[ed.dot], 
                                                 ed.point, start_col)
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
    key.C_n: next_line,
    key.C_p: prev_line,
    key.cr: open_line, 
    key.delete: delete_backward_char,
    key.bs: delete_backward_char, 
    key.C_d: delete_char,
    key.C_k: kill_line,
    key.C_w: kill_region,
    key.C_y: yank,
    key.C_l: refresh,
    key.C_x + key.C_a: append, # Enter dmacs append mode, exit with .
    # arrow keys, send ANSI escape sequences
    key.down: next_line,
    key.up: prev_line,}

def runcmd(keycode):
    """
    Execute a single pmacs command: dispatch on key k, run function
    """
    cmd = keymap[keycode]
    cmd(keycode)
    dmacs.prev_cmd = cmd
    # Note: A few cmd call el.runcmd we believe we needn't update el.prev_cmd

def clear_marker():
    edsel.put_marker(ed.dot, display.clear)
    display.put_cursor(edsel.tlines, 1)

def put_no_marker(bufline, attribs): 
    'Assign to edsel.put_marker to suppress marker while running pmacs'
    pass

def rpm():
    """
    pmacs editor: invoke editor functions with emacs control keys.
    Exit by typing M_x (that's alt X), like emacs 'do command'.

    rpm means 'raw pm' - this function requires terminal is already 
    in char mode ('raw' mode) and it does not restore line mode
    when it exits - so this rpm is the function to call from pysh,
    our custom Python shell.  Call pm (below) from the Python >>> prompt.
    """
    global inline
    dmacs.open_promptline()
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
                ed.buffer[ed.dot], ed.point = el.runcmd(k, ed.buffer[ed.dot],
                                              ed.point, start_col)
                dmacs.prev_cmd = el.prev_cmd
                # key.C_k and inline are handled in kill_line, above
                if k in (key.M_d, key.C_u): # M_d kill_word, C_u discard line 
                    inline = True
            elif k in dmacs.keymap:
                edsel.restore_cursor_to_cmdline()
                dmacs.runcmd(k)
                restore_cursor_to_window()
    dmacs.close_promptline()
    edsel.put_marker = saved_put_marker # initialized in except branch above
    edsel.put_marker(ed.dot, display.white_bg)
    edsel.restore_cursor_to_cmdline()


def pm():
    """ 
    pmacs editor: invoke editor functions with emacs control keys.
    Exit by typing M_x (that's alt X), like emacs 'do command'.

    This function assumes terminal is in line mode.
    It sets terminal character mode on entry and restores line mode on exit.
    So call this function from standard Python >>> prompt.
    Call rpm ('raw' pm) when terminal is already in char mode.
    So call rpm from our custom pysh >> prompt.
    """
    terminal.set_char_mode() 
    rpm() # raw pm, assumes term is already in char mode, doesn't restore mode
    terminal.set_line_mode()
