"""
sample.py - test ed.py API with example from ed.md: python sample.py
              additional commands confirm file got written and show its contents
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
D()

# confirm file got written, show its contents

B('test.txt')
print
p(1,S())
print
print 'Remove test.txt before running this again, to get the same results'
