"""
sample.py - test ed.py API with example from ed.md: python -i sample.py
              sample_read.py reads and displays the contents created here.
"""

from ed import *

B('test.txt')

a("""ed() enters ed command mode, with the : command  prompt.
'B <name>' creates a new buffer and loads the named file
'a' enters ed input mode and appends the text after the current line.
'w' writes the buffer contents back to the file
'q' quits ed command mode.
To quit input mode, type a period by itself at the start of a line.""")

w()
