"""
test_ed_pattern.py - Test ed.py pattern addresses using f and z functions

"""

from ed import *

print "B('ed.py.txt')"
B('ed.py.txt') 
print "l(0)"
l(0)

print """
Search forward - explicit pattern
"""
for i in range(4):
    print "l(f('text'))"
    l(f('text'))
    e()

print """
Search backward - explicit pattern
"""
for i in range(4):
    print "l(z(text))"
    l(z('text'))
    e()

print """
Search forward again - stored pattern
"""
print "l(0)"
l(0) # back to top
for i in range(4):
    print "l(f(''))"
    l(f(''))
    e()


print """
search backward - stored pattern
"""
for i in range(4):
    print "l(z(''))"
    l(z(''))
    e()
