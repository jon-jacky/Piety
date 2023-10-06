"""
editline.py - functions to edit and display a string with readline control keys.
  
Unlike readline, call and return for each key so you can edit without blocking.
"""

import string, re
import key, display
import terminal, keyseq # only needed by main() test 

# Define and initialize global variables used by editline.
# Conditinally exec only the *first* time this module is imported in a session.
# Then we can reload this module without re-initializing those variables.
# Must use EDPATH because PYTHONPATH only works for import, not open()
EDPATH = '/Users/jon/Piety/editors/' # FIXME? assign via env var or cmd line?
try:
    _ = point # if point is already defined, editlineinit was already exec'd
except:
    exec(open(EDPATH + 'editlineinit.py').read())

# used in main editing loop
printing_chars = string.printable[:-5] # exclude \t\n\r\v\f at the end

# used by forward word, backward word
start_word = re.compile(r'\W\w') # Non-word char then word char
end_word = re.compile(r'\w\W') # Word char then non-word char

# Functions that move point but do not change line contents

def move_to_point(point, line):
    # start_col accounts for prompt or other chars in left margin
    # move_to_column and start_col are 1-based but point is 0-based
    display.move_to_column(start_col + point + 1) # point is zero based
    return point, line

def move_beginning(point, line):
    point = 0
    return move_to_point(point, line)

def move_end(point, line):
    point = len(line.rstrip('\n')) # stop short of any final \n
    return move_to_point(point, line)

def backward_char(point, line):
    if point > 0:
        point -= 1
        display.backward_char()
    return point, line

def forward_char(point, line):
    if point < len(line) and line[point] != '\n':
        point += 1
        display.forward_char()
    return point, line

def forward_word(point, line):
    """
    Move to next non-word. char (space or punctuation) after word.
    FIXME? Does not move over last word to end of line, must use move_end.
    """
    m = end_word.search(line, point)
    if m:
        point = m.end() - 1 # space after word is end() of end_word pattern
        point, line = move_to_point(point, line)
    return point, line

def backward_word(point, line):
    """
    Move back to first char in preceding word (or this word).
    FIXME? Does not move over first word to start of line, use move_beginning.
    """
    m = end_word.search(line[point-1::-1],1) # search reversed str from point
    if m:
        point = point - m.start() - 1
        point, line = move_to_point(point, line)
    return point, line

# Functions that change line contents

def insert_char(keycode, point, line): # not in keymap so keycode arg is okay
    line = (line[:point] + keycode + line[point:])
    point += 1
    display.insert_char(keycode)
    return point, line

def delete_backward_char(point, line):
    if point > 0:
        line = (line[:point-1] + line[point:]) 
        point -= 1
        display.delete_backward_char()
    return point, line

def delete_char(point, line):
    line = (line[:point] + line[point+1:])
    display.delete_char() # point does not change
    return point, line

def kill_word(point, line):
    """
    Delete word, save in yank buffer.
    Repeat kill_word to save consecutive words in yank buffer.
    FIXME?  Does not delete last word in line, must use kill_line.
    """
    global yank_buffer
    m = end_word.search(line, point)
    if m:
        cut_word = line[point:m.start()+1]
        yank_buffer = (yank_buffer + cut_word if prev_cmd in kill_cmds
                       else cut_word)
        line = line[:point] + line[m.start()+1:]
        display.delete_nchars(point - (m.start()+1))
    return point, line

def kill_line(point, line):
    """
    Delete line from point to end-of-line, save in yank buffer.
    Append killed segment to yank buffer if we are doing consecutive kills.
    """
    global yank_buffer
    killed_segment = line[point:] # includes final \n, if any
    killed_newline = True if killed_segment.endswith('\n') else False
    killed_segment = killed_segment.rstrip('\n')
    if killed_segment: # Do not overwrite yank buffer with empty segment
        yank_buffer = (yank_buffer + killed_segment if prev_cmd in kill_cmds
                       else killed_segment)
    line = line[:point]
    display.kill_line()
    if killed_newline:
        line = line + '\n'
    return point, line

def discard(point, line): # name like gnu readline unix-line-discard
    """
    Delete line from start-of-line to point, save in yank buffer.
    Append killed segment to yank buffer if we are doing consecutive kills.
    """
    global yank_buffer
    killed_segment = line[:point]
    if killed_segment: # Do not overwrite yank buffer with empty segment
        yank_buffer = (yank_buffer + killed_segment if prev_cmd in kill_cmds
                       else killed_segment)
    line = line[point:]
    # FIXME below here is display updates, not working. Imitate kill_line ?
    point, line = move_beginning(point, line) # accounts for prompt, assigns pt
    display.putstr(line)
    display.kill_line() # remove any leftover text past line
    return move_beginning(point, line) # replace cursor again

# kill_cmds can't be defined until after we define kill_word etc.
kill_cmds = (kill_word, kill_line, discard) # cmds that update yank_buffer

def yank(point, line):
    'Paste (yank) string previously deleted by kill or discard'
    line = (line[:point] + yank_buffer + line[point:])
    point += len(yank_buffer)
    display.insert_string(yank_buffer)
    return point, line

def tab_n(n_spaces, point, line): # not in keymap so n_spaces arg is ok
    'Insert n spaces at point'
    spaces = ' ' * n_spaces
    line = line[:point] + spaces + line[point:]
    point += n_spaces
    display.insert_string(spaces)
    return point, line

def tab(point, line):
    'Insert standard number of spaces at point'
    return tab_n(n_spaces, point, line)

def refresh(point, line):
    'Display line and point - use after line has gotten scrambled or ...'
    display.move_to_column(start_col)
    display.putstr(line)
    display.kill_line() # remove any leftover text past line
    return move_to_point(point, line)

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
    key.C_u: discard,
    key.C_y: yank,
    key.M_f: forward_word,
    key.M_b: backward_word,
    key.M_d: kill_word,
    # arrow keys, send ANSI escape sequences
    key.left: backward_char,
    key.right: forward_char,
}

def elcmd(keycode, point, line):
    """
    Invoke a single editline command: look up key in keymap, run that command.
    """
    global prev_cmd
    if keycode in printing_chars:
        point, line = insert_char(keycode, point, line)
        prev_cmd = insert_char
    elif keycode in keymap:
        cmd = keymap[keycode]
        point, line = cmd(point, line) # local point, line here
        prev_cmd = cmd # must assign *after* calling cmd!
    else:
        display.putstr(key.bel) # FIXME makes no sound - why?
    return point, line

def elglob(keycode):
    """
    Invoke single editine command, update immutable global variables.
    """
    global point, line
    point, line = elcmd(keycode, point, line) # point, line are immutable

def runcmd(keycode, buffer, dot):
    """
    Invoke single editline command, update mutable buffer array parameter.
    """
    global point
    point, buffer[dot] = elcmd(keycode, point, buffer[dot]) # buffer is mutable

def el():
    """
    Test editline on the Python command line: loop invoking editor commands.
    Type characters and control keys to edit inline, exit with M-x.
    Comment/uncomment lines to switch between using elglob and runcmd.
    """
    global point, line,  prev_cmd
    terminal.set_char_mode()
    # refresh(point, line) # immutable line, updated by eglob
    refresh(point, buffer[dot]) # mutable buffer, updated by runcmd
    while True:
        c = terminal.getchar()
        k = keyseq.keyseq(c)
        if k: # keyseq returns '' if key sequence is not complete
            if k == key.M_x:
                break
            else:
                # elglob(k) # update global immutable vars: point, line
                runcmd(k, buffer, dot) # update mutable parameter: buffer
    terminal.set_line_mode()
    print() # advance to next line for Python prompt

