"""
display - Update the terminal display using ANSI control sequences.
"""

from util import putstr # write without newline, flush for immediate output

esc = '\x1B'     # \e does not work 'invalid \x escape'
csi = esc+'['    # ANSI control sequence introducer

cha = csi+'%dG'  # cursor horizontal absolute, column %d
cub = csi+'D'    # cursor backward (left), default 1 char
cuf = csi+'C'    # cursor forward (right), default 1 char
cup = csi+'%d;%dH' # cursor position %d line, %d column
dch = csi+'%dP'  # delete chars, remove %d chars at current position
ed  = csi+'J'    # erase display from cursor to end
el  = csi+'%dK'  # erase in line, %d is 0 start, 1 end, or 2 all
el_end = el % 0  # 0: erase from cursor to end of line
el_all = el % 2  # 2: erase entire line
ich = csi+'%d@'  # insert chars, make room for %d chars at current position
decstbm = csi+'%d;%dr' # DEC Set Top Bottom Margins (set scrolling region
                 # %d,%d is top, bottom, so 23;24 is bottom two lines
                 # then it sets cursor at the top of the page
decstbmn  = csi+';r' # decstbm default: set scrolling region to full screen

sgr = csi + '%s' + 'm' # set graphic rendition. %s is ;-separated integers like
                 # bold+inverse: esc[0;1;7m by sgr % ';'.join('017')

# sgr, attribute values
clear = 0        # clears attributes (not transparent!)
white_bg = 47    # gray on mac terminal
bold = 1
blink = 5

def attrs(*attributes):
    """
    Convert variable length arg list of integers to ansi attributes string
    Then the sgr control sequence is just sgr % attrs(*attributes)
    """
    return ';'.join([ str(i) for i in attributes ])

def render(text, *attributes):
    """
    Print text with one or more attributes, each given by separate int arg,
    then clear attributes, but do not print newline.
    """
    putstr(sgr % attrs(*attributes) + text + sgr % attrs(clear))

# used by line

def self_insert_char(key):
    'Insert character in front of cursor'
    putstr((ich % 1) + key) # open space to insert char

def delete_char():
    'Delete character under the cursor'
    putstr(dch % 1)

def backward_delete_char():
    'Delete character before cursor'
    putstr(cub + dch % 1)

def forward_char():
    putstr(cuf) # move just one char

def backward_char():
    putstr(cub)

def move_to_column(column):
    putstr(cha % column)

# line also uses kill_line, defined below

# used by edsel and window, they also use render (above)

def erase_display(): # name in gnu readline
    putstr(ed)

def put_cursor(line, column):      # not in emacs or gnu readline
    putstr(cup % (line, column))

def kill_line():
    'Erase from cursor to end of line'
    putstr(el_end)

def kill_whole_line():
    'Erase entire line'
    putstr(el_all)

def set_scroll(ltop, lbottom): 
    'Set scrolling region to lines ltop through lbottom (line numbers)'
    putstr(decstbm % (ltop, lbottom))

def set_scroll_all():
    'Set scrolling region to entire display'
    putstr(decstbmn)

def put_render(line, column, text, *attributes):
    """
    At line, column, print text with attributes
    but without newline, then clear attributes.
    """
    put_cursor(line, column)
    putstr(sgr % attrs(*attributes) + text + sgr % attrs(clear))
