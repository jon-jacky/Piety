"""
test_ed_D.py - test D and DD delete buffer commands

"""

from ed import *

print' Test D with unsaved changes, then DD on current buffer'
print

print "B('new.txt')"
B('new.txt')
print

print "i('Here is a line')"
i('Here is a line')
print

print "n()"
n()
print

print "D()"
D()
print

print "DD()"
DD()
print

print "n()"
n()
print


print' Test D with saved changes on current buffer'
print

print "B('new1.txt')"
B('new1.txt')
print

print "i('Here is a line')"
i('Here is a line')
print

print "n()"
n()
print

print "w()"
w()
print

print "D()"
D()
print

print "n()"
n()
print


print 'Test D with saved changes on a different buffer'
print

print "B('new2.txt')"
B('new2.txt')
print

print "i('Here is a line')"
i('Here is a line')
print

print "n()"
n()
print

print "w()"
w()
print

print "b('scratch')"
b('scratch')
print "n()"
n()
print

print "D('new2.txt')"
D('new2.txt')
print

print "n()"
n()
print

print "Remove new1.txt, new2.txt before running script again to obtain same results"
