"""
sample_ed_cmd.py - test ed.py API with example from ed.md
                    but here use ed_cmd.  python sample_ed_cmd.py

The output should look the same as the output from sample.py (in sample.log)
"""

from ed import *

ed_cmd('e test.txt')
ed_cmd('a')
ed_cmd('ed() enters ed command mode.  By default, there is no command prompt.')
ed_cmd("'e <name>' loads the named file into the current buffer.")
ed_cmd("'a' enters ed input mode and appends the text after the current line.")
ed_cmd("'w' writes the buffer contents back to the file")
ed_cmd("'q' quits ed command mode.")
ed_cmd('To quit input mode, type a period by itself at the start of a line.')
ed_cmd('.')

ed_cmd('w')

# confirm file got written, read into a different buffer and print

ed_cmd('B test.txt')
print
ed_cmd('1,$p')
ed_cmd('q')
print
print 'Remove test.txt before running this again, to get the same results'
