"""
editline.py - functions to edit and display a string with readline control keys.
  
Unlike readline, call and return for each key so you can edit without blocking.
Each function takes current point (integer index) and line (string) arguments
and returns the updated point and line.
"""

import string, re
import key, display
import util, terminal, keyseq # only needed by main() test 
# used by forward word, backward word
start_word = re.compile(r'\W\w') # Non-word char then word char
end_word = re.compile(r'\w\W') # Word char then non-word char

# start_col = 2  # prompt is '> '
start_col = 0    # default, no prompt or other chars at left margin

def move_to_point(point, line):
    # start_col accounts for prompt or other chars in left margin
    # move_to_column and start_col are 1-based but point is 0-based
    display.move_to_column(start_col + point + 1) # point is zero based
    return point, line

def move_beginning(point, line):
    point = 0
    return move_to_point(point, line)

def move_end(point, line):
    point = len(line)
    return move_to_point(point, line)

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

def backward_char(point, line):
    if point > 0:
        point -= 1
        display.backward_char()
    return point, line

def delete_char(point, line):
    line = (line[:point] + line[point+1:])
    display.delete_char() # point does not change
    return point, line

def forward_char(point, line):
    if point < len(line):
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

def kill_word(point, line):
    """
    Delete word, save in yank buffer.
    FIXME?  Does not delete last word in line, must use kill_line.
    """
    global yank_buffer
    m = end_word.search(line, point)
    if m:
        inline_yank = True
        cut_word = line[point:m.start()+1]
        # repeat kill_word to append successive words to yank buffer
        yank_buffer = (yank_buffer + cut_word if prev_fcn in cut_fcns
                       else cut_word)
        line = line[:point] + line[m.start()+1:]
        display.delete_nchars(point - (m.start()+1))
    return point, line

def kill_line(point, line):
    'Delete line from point to end-of-line, save in yank buffer'
    global yank_buffer
    inline_yank = True
    killed_segment = line[point:]
    if killed_segment: # Do not overwrite yank buffer with empty segment
        yank_buffer = killed_segment
    line = line[:point] # point does not change
    display.kill_line()
    return point, line

def discard(point, line): # name like gnu readline unix-line-discard
    'Delete line from start-of-line to point'
    global yank_buffer
    inline_yank = True
    killed_segment = line[:point]
    if killed_segment: # Do not overwrite yank buffer with empty segment
        yank_buffer = killed_segment
    line = line[point:]
    point, line = move_beginning(point, line) # accounts for prompt, assigns pt
    util.putstr(line)
    display.kill_line() # remove any leftover text past line
    return move_beginning(point, line) # replace cursor again

prev_fcn = None
cut_fcns = (kill_word, kill_line, discard)

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

n_spaces = 4 # Used by tab, below.  In production use sked.indent.

def tab(point, line):
    'Insert standard number of spaces at point'
    return tab_n(n_spaces, point, line)

def refresh(point, line):
    'Display line and point - use after line has gotten scrambled or ...'
    display.move_to_column(start_col)
    util.putstr(line)
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
}

# globals used by main
line = ''
point = 0
printing_chars = string.printable[:-5] # exclude \t\n\r\v\f at the end
inline_yank = True
yank_buffer = ''

def main():
    """
    Test keys and functions in editline keymap table.  Also insert_char, key.cr
    This function is closely based on the dm function in the dmacs module.
    Enter string to edit at prompt, then type chars and ctrl keys, RET to exit.
    """
    global prev_fcn, point, line
    line = input('Line to edit: ')
    point = len(line)
    util.putstr(line)
    # open_promptline() # from dmacs dm(), not used here
    terminal.set_char_mode()
    while True:
        c = terminal.getchar()
        k = keyseq.keyseq(c)
        if k: # keyseq returns '' if key sequence is not complete
            if k == key.cr:
                break
            elif k in printing_chars:
                point, line = insert_char(k, point, line)
                prev_fcn = insert_char
            elif k in keymap:
                fcn = keymap[k]
                point, line = fcn(point, line)
                prev_fcn = fcn
            else:
                util.putstr(key.bel) # FIXME makes no sound - why?
    terminal.set_line_mode()
    # close_promptline() # from dmacs dm(), not used here
    # display.put_cursor(edsel.tlines, 1) # return cursor to command line # dm
    print('\n'+line)

if __name__ == '__main__':
    main()
