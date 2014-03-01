"""
test_ed_s.py - Test ed.py s(ubstitute) command
               
This test works on internal buffer only, no files: python test_ed_s.py

"""

from ed import *

a("""ed is an editor based on the classic Unix editor ed.
Again we mention ed.  This is test of ed.
In this line there is no mention of it.
In this line there is a single mention of ed.
And in this last line we mention ed, then ed again, twice altogether.""")
print

p(1,S())
print

p()
print

# Try all combinations of args

s('ed','emacs')
p()
print

s('emacs','vi',False)
p()
print

s(1,'ed','emacs')
p()
print

s(1,'emacs','vi',False)
p()
print

s(1,'emacs','ed')
p(1)
print

s(2,4,'ed','vi')
p(1,S())
print

s(2,4,'vi','emacs',False)
p(1,S())
print
