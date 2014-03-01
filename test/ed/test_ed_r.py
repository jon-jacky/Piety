"""
test_r.py - Test ed.py r(ead)

 python -i test_ed_r.py

These tests don't write any files, so you needn't delete anything afterward.

"""

from ed import *

a("""Line 0
Line 1
Line 2""")
p(1,S())
print

e()
print

r()
print

r(101,"rtest0.txt")
print

r("rtest0.txt")
print
p(1,S())
print

r(1,"rtest1.txt")
print
p(1,S())
