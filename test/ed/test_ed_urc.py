"""
test_ed_urc.py - Test ed.py functions b(uffer), r(ead), c(hange)

 python -i test_ed_urc.py

These tests don't write any files, so you needn't delete anything afterward.

"""

from ed import *
from test_cmd import test_cmd

test_cmd(b, 'create buffer', 'new.txt')

print "> n() # print buffers"
n()
print

test_cmd(r, 'read file into empty buffer', 'test_cmd.py')

print "> l(10) # advance to line 9 and print it"
l(10)
print

test_cmd(r, 'read file into middle of buffer', 'README.md.txt')

print "> p() # print the current line"
p()
print

test_cmd(c, 'change the current line', '### This is the changed line ###')

test_cmd(c, 'replace all the remaining lines', 
         o(),S(), '### This line replaces all that followed ###')
