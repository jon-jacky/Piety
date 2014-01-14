"""
test_ed_pattern.py - Test ed.py pattern addresses

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
    print "l('/text/')"
    l('/text/')
    m()

print """
Search backward - explicit pattern
"""
for i in range(4):
    print "l('?text?')"
    l('?text?')
    m()

print """
Search forward again - stored pattern
"""
print "l(0)"
l(0) # back to top
for i in range(4):
    print "l('//')"
    l('/text/')
    m()


print """
search backward - stored pattern
"""
for i in range(4):
    print "l('??')"
    l('??')
    m()
