"""
test_ed_small.py  - test, demonstrate Python API for the text editor ed.py
                     Test on small buffers of 0, 1, 2 lines

Run this script from the directory above Piety, it uses relative paths:

 python -i Piety/samples/test_ed_small.py

 Remove test_ed_small.txt before running this script again,
  to obtain the same results

"""

from ed import *
from test_cmd import test_cmd

test_cmd(B, 'open new file', 'test_ed_small.txt')
test_cmd(i, 'insert line in empty file', 'Line i')
test_cmd(d, 'delete line from one-line file', ()) # no args
test_cmd(a, 'append line in empty file', 'Line a')
test_cmd(d, 'delete line from one-line file', ()) # no args
test_cmd(i, 'insert line in empty file', 'Line i')
test_cmd(a, 'append line in one-line file', 'Line a')
test_cmd(w, 'write two line file', ())
test_cmd(d, 'delete last line from two-line file', ())
test_cmd(i, 'insert line at start of one-line file', 'Line ii')
test_cmd(w, 'write two line file with different name', 'test_ed_small_2.txt')
test_cmd(d, 'delete first line from two-line file', ())

# Test new b,c command

test_cmd(b, 'Create new buffer', 'new.txt')
test_cmd(a, 'Add first line to empty buffer', 'Line 1')
test_cmd(a, 'Add second line to one-line buffer', 'Line 2')
test_cmd(c, 'Change last line in two-line buffer', 'Changed line 2')
test_cmd(c, 'Change first line in two-line buffer', 0, 'Changed line 1')

print """# Remove test_ed_small.txt and test_ed_small_2.txt
# before running this script again, to obtain the same result
"""
