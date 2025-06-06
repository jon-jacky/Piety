"""
editline.py - functions to edit and display a string with readline control keys.
  
Unlike readline, call and return for each key so you can edit without blocking.

This is the revised version which can edit text in a window on the left without
disturbing text displayed in an adjacent window on the right.   The original
version lives on, renamed but otherwise unchanged, in tasking/editcommand.py.
Most of this revised editline duplicates code in the original editcommand.
"""

import string, re
import key, display
import edsel # needed for edsel.width
import terminal, keyseq # only needed by test 

# Define and initialize global variables used by editline,
# but only the *first* time this module is imported in a session.
# Then we can reload this module without re-initializing those variables.
try:
    _ = n_spaces # if already defined, editline was already imported
except:
    n_spaces = 4 # Used by tab.
    killed = str() # saved killed (cut) words, can be restored with yank (paste)
    prev_cmd = None # some functons behave differently when repeated

# used in main editing loop
printing_chars = string.printable[:-5] # exclude \t\n\r\v\f at the end

# used by forward word, backward word
start_word = re.compile(r'\W\w') # Non-word char then word char
end_word = re.compile(r'\w\W') # Word char then non-word char

# Functions that replace functions from the display module that
# insert and delete text on the display, that disturb text 
# displayed in an adjacent window to the right.
# These replacement functions ovewrite text and pad with blanks
# to limit their effects within the width of the current window,
# so they can work alongside another window.
# Naming convention: display.insert_string -> display_insert_string etc.

def display_insert_string(string, line, point):
    """
    Display effect of inserting string into line on display at cursor position,
    achieved by overwriting display from cursor position  with string + suffix 
    Assumes line on display past suffix is already blank-padded to window edge. window edge.
    Takes line, point as input args but returns nothing, just updates display.
    """ 
    suffix = line[point:].rstrip('\n') # text after inserted string
    rwidth = edsel.width - point # space remaining in window past cursor
    display.putstr((string + suffix)[:rwidth]) # clip to window width
    move_to_point(point, edsel.start_col) # return from end of suffix to point
    # FIXME? edsel.start_col here, not passed parameter as usual in this module
        
def display_delete_nchars(nchars, line, point):
    """
    Display effect of deleting chars from line on display at cursor position,
    achieved by overwriting display from cursor position  with suffix + spaces.
    Assumes line on display past suffix was already blank-padded to window edge. window edge.
    Takes line, point as input args but returns nothing, just updates display.
    """ 
    suffix = line[point:].rstrip() # text after deleted string
    padding = ' '*nchars # spaces added after suffix that replace deleted string
    rwidth = edsel.width - point # space remaining in window past cursor
    display.putstr((suffix + padding)[:rwidth]) # clip, shouldn't be needed
    move_to_point(point, edsel.start_col) # return from end of padding to point
    # FIXME? edsel.start_col here, not passed parameter as usual in this module
                 
# Function that updates line and point but does not appear in keymap table

def insert_char(keycode, line, point):
    line = (line[:point] + keycode + line[point:])
    point += 1
    #display.insert_char(keycode)
    display_insert_string(keycode, line, point)    
    return line, point
 
# Helper function, does not appear in keymap table
# Updates display but does not update any variables so it does not return any.
 
def move_to_point(point, start_col):
    # start_col accounts for prompt or other chars in left margin
    # move_to_column and start_col are 1-based but point is 0-based
    # So we DON'T need + 1 here because it's already included in start_col
    display.move_to_column(start_col + point) # + 1) NOT! +1 not needed here

# Functions that appear in the keymap table must all have the same arguments
# and the same returned variables, even though many do not use all of them.
 
# Functions that appear in keymap table
# that move point but do not change line contents
# We still must pass and return line because these appear in keymap table

def move_beginning(line, point, start_col):
    point = 0
    move_to_point(point, start_col)
    return line, point

def move_end(line, point, start_col):
    point = len(line.rstrip('\n')) # stop short of any final \n
    move_to_point(point, start_col)
    return line, point

def backward_char(line, point, start_col):
    if point > 0:
        point -= 1
        display.backward_char()
    return line, point

def forward_char(line, point, start_col):
    if point < len(line) and line[point] != '\n':
        point += 1
        display.forward_char()
    return line, point

def forward_word(line, point, start_col):
    """
    Move to next non-word. char (space or punctuation) after word.
    FIXME? Does not move over last word to end of line, must use move_end.
    """
    m = end_word.search(line, point)
    if m:
        point = m.end() - 1 # space after word is end() of end_word pattern
        move_to_point(point, start_col) 
    return line, point

def backward_word(line, point, start_col):
    """
    Move back to first char in preceding word (or this word).
    FIXME? Does not move over first word to start of line, use move_beginning.
    """
    m = end_word.search(line[point-1::-1],1) # search reversed str from point
    if m:
        point = point - m.start() - 1
        move_to_point(point, start_col)
    return line, point

# Functions that appear in keymap table and change line contents

def delete_char(line, point, start_col):
    line = (line[:point] + line[point+1:])
    # display.delete_char() # point does not change
    display_delete_nchars(1, line, point)
    return line, point

def delete_backward_char(line, point, start_col):
    """
    Code from backward_char body followed by code for delete_char body
    """
    # backward char body
    if point > 0:
        point -= 1
        display.backward_char()
    else:
        return line, point
     # delete_char body
    line = (line[:point] + line[point+1:])
    # display.delete_char() # point does not change
    display_delete_nchars(1, line, point)
    return line, point
     
def kill_word(line, point, start_col):
    """
    Delete word, save in killed buffer.
    Repeat kill_word to save consecutive words in killed buffer.
    FIXME?  Does not delete last word in line, must use kill_line.
    """
    global killed
    m = end_word.search(line, point)
    if m:
        killed_word = line[point:m.start()+1]
        killed = (killed + killed_word if prev_cmd in kill_cmds
                       else killed_word)
        line = line[:point] + line[m.start( )+1:]
        # The following commented-out line works on Mac but not ChromeBook
        # It seems Mac term tolerates negative argument but CB Term does not.
        # display.delete_nchars(point - (m.start()+1)) # FIXME? args reversed?
        display_delete_nchars(len(killed_word), line, point)
    return line, point

def kill_line(line, point, start_col):
    """
    Delete line from point to end-of-line, save in killed buffer.
    Append killed segment to killed buffer if we are doing consecutive kills.
    """
    global killed
    killed_segment = line[point:] # includes final \n, if any
    killed_newline = True if killed_segment.endswith('\n') else False
    killed_segment = killed_segment.rstrip('\n')
    if killed_segment: # Do not overwrite killed buffer with empty segment
        killed = (killed + killed_segment if prev_cmd in kill_cmds
                       else killed_segment)
    line = line[:point]
    # display.kill_line()
    edsel.blank_line(len(killed_segment.rstrip('\n')))
    move_to_point(point, edsel.start_col) # return from end of padding to point
    if killed_newline:
        line = line + '\n'
    return line, point

def discard_line(line, point, start_col): # name like gnu readline unix-line-discard
    """
    Delete line from start-of-line to point, save in killed buffer.
    Append killed segment to killed buffer if we are doing consecutive kills.
    """
    global killed
    killed_segment = line[:point]
    if killed_segment: # Do not overwrite killed buffer with empty segment
        killed = (killed + killed_segment if prev_cmd in kill_cmds
                       else killed_segment)
    line = line[point:]
    point = 0
    refresh(line, point, start_col)
    return line, point

# kill_cmds can't be defined until after we define kill_word etc.
kill_cmds = (kill_word, kill_line, discard_line) # cmds that update killed

def yank(line, point, start_col):
    'Yank (paste) string(s) deleted by kill_word, kill_line, or discard_line'
    line = (line[:point] + killed + line[point:])
    point += len(killed)
    # display.insert_string(killed)
    display_insert_string(killed, line, point)
    return line, point

def tab_n(n_spaces, line, point): # n_spaces arg ok because tab_n is not in keymap
    'Insert n spaces at point'
    spaces = ' ' * n_spaces
    line = line[:point] + spaces + line[point:]
    point += n_spaces
    # display.insert_string(spaces)
    display_insert_string(spaces, line, point)
    return line, point

def tab(line, point, start_col):
    'Insert standard number of spaces at point'
    line, point= tab_n(n_spaces, line, point)
    return line, point

def refresh(line, point, start_col):
    'Display line and point - use after line has gotten scrambled or ...'
    display.move_to_column(start_col) # +1) not needed, start_col is 1-based
    # display.putstr(line.rstrip('\n'))
    # display.kill_line() # remove any leftover text past line
    edsel.display_padded(line) 
    move_to_point(point, start_col)
    return line, point # neither of these is updated

keymap = {
    key.bs: delete_backward_char, # C_h
    key.delete: delete_backward_char,
    key.htab: tab, # C_i
    key.C_a: move_beginning,
    key.C_b: backward_char,
    key.C_d: delete_char,
    key.C_e: move_end,
    key.C_f: forward_char,
    # key.C_h is key.bs above
    # key.C_i is key.htab above
    key.C_k: kill_line,
    key.C_l: refresh,
    key.C_u: discard_line,
    key.C_y: yank,
    key.M_f: forward_word,
    key.M_b: backward_word,
    key.M_d: kill_word,
    # arrow keys, send ANSI escape sequences
    key.left: backward_char,
    key.right: forward_char,
}

def runcmd(keycode, line, point, start_col):
    """
    Invoke a single editline command: look up key in keymap, run that command.
    """
    global prev_cmd
    if keycode in printing_chars:
        line, point = insert_char(keycode, line, point)
        prev_cmd = insert_char
    elif keycode in keymap:
        cmd = keymap[keycode]
        line, point = cmd(line, point, start_col)
        prev_cmd = cmd # must assign *after* calling cmd!
    else:
        display.putstr(key.bel)
    return line, point
 
def el():
    """
    Test editline on the Python command line: loop invoking editor commands.
    Type characters and control keys to edit inline, exit with M-x.
    """
    global prev_cmd

    # previously these were globals
    line = '' # for test el() below
    point = 0 # zero-based index into line, a Python string
    prompt = '> '
    start_col = 3 # one-based index of character after prompt on terminal
    
    terminal.set_char_mode()
    display.putstr(prompt)
    refresh(line, point, start_col)
    while True:
        c = terminal.getchar()
        k = keyseq.keyseq(c)
        if k: # keyseq returns '' if key sequence is not complete
            if k == key.M_x:
                break
            else:
                line, point = runcmd(k, line, point, start_col)
    terminal.set_line_mode()
    print() # advance to next line to print
    print(line)
    
