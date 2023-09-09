"""
pmacs.py - display editor that uses emacs control terminal, keys.

pmacs might mean 'Python emacs' but actually means 'poor emacs'
or 'pathetic emacs' or maybe 'Passing grade emacs, just above Fail'.
"""

import terminal, key, keyseq, display, edsel, dmacs, editline 
import sked as ed

# Some functions do not use keycode arg but pmcmd and pm require it to be there

def open_line(keycode):
    """
    Split line at point, replace line in buffer at dot
    with its prefix, append suffix after line at dot.
    """
    suffix = ed.buffer[ed.dot:] # including final \n
    # Calls editline.kill_line, thanks to key.C_k, not keycode
    editline.elcmd_aref(key.C_k, ed.buffer, ed.dot)
    ed.buffer[ed.dot+1:ed.dot+1] = suffix # sic, insert suffix after dot
    ed.dot = ed.dot + 1
    editline.point = 0
    edsel.update_below(ed.dot) # update display
    # may need more after update_below - see edsel display_y and other uses
# The following functions supercede and wrap functions in editline

def join_prev():
    'Join this line to previous. At first line do nothing.'
    if ed.dot > 1:
        editline.point = len(ed.buffer[ed.dot-1])-1 # don't count \n
        ed.j(ed.dot-1, ed.dot)

def delete_backward_char(keycode):
    """
    If point is not at start of line, delete preceding character.
    Otherwise join to previous line.  At start of first line do nothing.
    """
    if editline.point > 0:
        # Calls editline.delete_backward_char, thanks to keycode
        editline.elcmd_aref(keycode, ed.buffer, ed.dot)
    else: 
        join_prev() # see above

def join_next():
    'Join next line to this one. At last line do nothing.'
    if ed.dot < ed.S():
        ed.j() # defaults in ed.j join dot to dot+1

def delete_char(keycode):
    """
    If point is not at end of line, delete character under cursor.
    Otherwise join next line to this one.  At end of last line do nothing.
    """
    if editline.point < len(ed.buffer[ed.dot]):
        # Calls editline.delete_char, thanks to keycode
        editline.elcmd_aref(keycode, ed.buffer, ed.dot)
    else:
        join_next() # see above

yank_lines = True # initially when module loaded, reassigned while editing

def kill_line(keycode):
    """
    Kill entire line(s) or kill the rest of line at dot
    """
    global yank_lines
    if editline.point == 0:  # cursor at beginning of line, kill whole line
        yank_lines = True
        dmacs.kill_line()
    else:
        yank_lines = False # cursor within line, only kill from cursor to end
        # Calls editline kill_line, thanks to keycode
        editline.elcmd_aref(keycode, ed.buffer, ed.dot)

def cut(keycode):
    global yank_lines
    yank_lines = True
    dmacs.in_region(edsel.d)

def yank(keycode):
    """
    Yank entire line(s) or yank word(s) within a line, depending on yank_lines
    """
    if yank_lines:
        ed.y() # yank entire line(s)
    else:
        # Calls editline.yank, thanks to keycode
        editline.elcmd_aref(keycode, ed.buffer, ed.dot)

def refresh(keycode):
    'pmacs refresh requires keycode arg but edsel refresh has none.'
    edsel.refresh()

# FIXME? add command to enter edsel/sked append mode?

keymap = {
    key.cr: open_line, 
    key.delete: delete_backward_char,
    key.bs: delete_backward_char, 
    key.C_d: delete_char,
    key.C_k: kill_line,
    key.C_w: cut, 
    key.C_y: yank,
    key.C_l: refresh,
}
def pmcmd(keycode):
    """
    Execute a single pmacs command: dispatch on key k, run function
    """
    fcn = keymap[keycode]
    fcn(keycode)

def restore_cursor_to_window():
    # point+1 to make put_cursor call consistent with editline move_to_column
    display.put_cursor(edsel.wline(ed.dot), editline.point + 1)

def pm():
    """
    pmacs editor: invoke editor functions with emacs control keys.
    Exit by typing M_x (that's alt X), like emacs 'do command'.
    """
    global yank_lines
    dmacs.open_promptline()
    terminal.set_char_mode()
    edsel.restore_cursor = restore_cursor_to_window
    edsel.restore_cursor()
    while True:
        c = terminal.getchar()
        k = keyseq.keyseq(c)
        if k: # keyseq returns '' if key sequence is not complete
            if k == key.M_x:
                break
            elif k in keymap:
                pmcmd(k)
            elif k in editline.printing_chars or k in editline.keymap:
                editline.elcmd_aref(k, ed.buffer, ed.dot)
                yank_lines = False # editing inline, yank word(s) into line
            elif k in dmacs.keymap:
                dmacs.dmcmd(k)
    dmacs.close_promptline()
    edsel.restore_cursor = edsel.restore_cursor_to_cmdline
    edsel.restore_cursor()
    terminal.set_line_mode()
