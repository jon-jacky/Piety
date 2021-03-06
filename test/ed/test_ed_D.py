"""
test_ed_D.py - test D and X delete buffer commands

"""

from ed import *

print(' Test D with unsaved changes, then repeat D on current buffer')
print()

print("B('new.txt')")
B('new.txt')
print()

print("i('Here is a line')")
i('Here is a line')
print()

print("n()")
n()
print()

print("D()")
D()
print()

print("D() again")
D()
print()

print("n()")
n()
print()


print(' Test D with saved changes on current buffer')
print()

print("B('new1.txt')")
B('new1.txt')
print()

print("i('Here is a line')")
i('Here is a line')
print()

print("n()")
n()
print()

print("w()")
w()
print()

print("D()")
D()
print()

print("n()")
n()
print()


print('Test D with saved changes on a different buffer')
print()

print("B('new2.txt')")
B('new2.txt')
print()

print("i('Here is a line')")
i('Here is a line')
print()

print("n()")
n()
print()

print("w()")
w()
print()

print("b('main')")
b('main')
print("n()")
n()
print()

print("D('new2.txt')")
D('new2.txt')
print()

print("n()")
n()
print()

print("Remove new1.txt, new2.txt before running script again to obtain same results")
