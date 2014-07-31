"""
ansi.py - Define ANSI terminal control codes and functions that use them.

Best explanation at:
 http://www.inwap.com/pdp10/ansicode.txt.  
 especially section "Minimum requirements for VT100 emulation"
See also:
 http://en.wikipedia.org/wiki/ANSI_escape_code
 http://invisible-island.net/xterm/ctlseqs/ctlseqs.html
Other pages with the same information in different formats:
 http://ascii-table.com/ansi-escape-sequences.php
 http://www.sweger.com/ansiplus/EscSeq.html
This page says 'Line and column numbers start at 1':
 http://www.umich.edu/~archive/apple2/misc/programmers/vt100.codes.txt
"""

import re
from ascii import esc

csi = esc+'['    # control sequence introducer

# Inputs: arrow keys
cuu1 = csi+'A'  # cursor up, default 1 char
cud1 = csi+'B'  # cursor down, default 1 char
cuf1 = csi+'C'  # cursor forward, default 1 char
cub1 = csi+'D'  # cursor backward, default 1 char

# Outputs with parameters

cuf = csi+'%dC'  # cursor forward %d characters
cub = csi+'%dD'  # cursor backward %d characters
cha = csi+'%dG'  # cursor horizontal absolute, column %d
cup = csi+'%d;%dH' # cursor position %d line, %d column

ich = csi+'%d@'  # insert chars, make room for %d chars at current position
dch = csi+'%dP'  # delete chars, remove %d chars at current position

el  = csi+'%dK'  # erase in line, %d 0: erase from cursor to end of line
                 #                %d 1: erase from start of line to cursor
                 #                %d 2: erase entire line

ed  = csi+'J'    # erase display from cursor to end

decstbm = csi+'%d;%dr' # DEC Set Top Bottom Margins (set scrolling region)
                       # %d,%d is top, bottom, so 23;24 is bottom two lines
                       # then it sets cursor at the top of the page

decstbmn  = csi+';r' # decstbm default: set scrolling region to full screen

# sgr, set graphic rendition, special cases
sgri = csi+'7m'  # set reverse video (set graphic rendition - inverse video)
sgr0 = csi+'0m'  # clear reverse video (set graphic rendition - clear all)

# sgr, general case
sgr = csi + '%s' + 'm' # set graphic rendition. %s is ;-separated integers like
                 # bold+inverse: esc[0;1;7m by ansi.sgr % ';'.join('017')

# sgr, attribute values
clear = '0'      # clears attributes (not transparent!)
bold = '1'
dim = '2'        # no effect in mac term by itself, dim with background color
italic = '3'     # no effect in mac terminal
underine = '4'
blink_slow = '5' # ouch! blinks - very irritating
blink_fast = '6' # doesn't blink in mac terminal
inverse = '7'
concealed = '8' # 'do not display character echoed locally' - ?
reserved = '9' # 'reserved for future standardization'
primary_font = '10' # LA100
alternate_font = '11' # LA100 had alternate fonts 11 - 19
clear_bold = '22' # clear bold or dim only
clear_underline = '24' # clear underline only
clear_blink = '25' # clear slow or fast blink only
clear_inverse = '27' # clear inverse only
black = '30' # write with black
red = '31'   # etc. ...
green = '32'
yellow = '33'
blue = '34'
magenta = '35'
cyan = '36'
white = '37'    # gray on mac terminal
black_bg = '40' # set background to black
red_bg = '41'
green_bg = '42'
yellow_bg = '43'
blue_bg = '42'
magenta_bg = '45'
cyan_bg = '46'
white_bg = '47'  # gray on mac terminal

def setgr(*attributes):
    'set graphic rendition, each attribute is a separate string arg'
    print(sgr % ';'.join(attributes)), # do not print newline at the end

def setgri(*iattributes):
    'set graphic rendition, each attribute is a separate integer arg'
    setgr(*[ str(i) for i in iattributes ])

def cleargr():
    'clear all ansi sgr attributes'
    print sgr0, '', # without final '' bg color continues to end of line

def render(text, *attributes):
    'Print text with one or more attributes, each specified a separate int arg'
    setgri(*attributes)
    print text,
    cleargr()

# regex from https://github.com/helgefmi/ansiterm/blob/master/ansiterm.py 
ctlseq = re.compile(r'^\x1b\[?([\d;]*)(\w)')

if __name__ == '__main__':
    for i in range(1,8) + range(30,38) + range(41,48): # b/w, fg colors, bg
        render('Demonstrating ansi sgr attribute %d' % i, i)
        print # each demo on its own line
    for i in range(41,48): # bgcolors
        for j in (2,1): # dim, bold
            render('Demonstrating ansi sgr attributes %d, %d' % (i,j), i, j)
            print
