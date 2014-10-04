"""
sample_ed_cmd.py - test ed.py API with example from ed.md
                    but here use ed_cmd.  python sample_ed_cmd.py

The output should look the same as the output from sample.py (in sample.log)
"""

import ed

ed.cmd('e test.txt')
ed.cmd('a')
ed.cmd('ed() enters ed command mode.  By default, there is no command prompt.')
ed.cmd("'e <name>' loads the named file into the current buffer.")
ed.cmd("'a' enters ed input mode and appends the text after the current line.")
ed.cmd("'w' writes the buffer contents back to the file")
ed.cmd("'q' quits ed command mode.")
ed.cmd('To quit input mode, type a period by itself at the start of a line.')
ed.cmd('.')

ed.cmd('w')

# confirm file got written, read into a different buffer and print

ed.cmd('B test.txt')
print
ed.cmd('1,$p')
ed.cmd('q')
print
print 'Remove test.txt before running this again, to get the same results'
