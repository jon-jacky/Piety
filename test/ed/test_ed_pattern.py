"""
test_ed_pattern.py - Test ed.py pattern addresses using f and z functions

"""

from ed import *

print("B('ed.py.txt')")
B('ed.py.txt') 
print("l(1)")
l(1)

print("""
Search Forward - explicit pattern
""")
for i in range(4):
    print("l(F('text'))")
    l(F('text'))
    b()

print("""
Search backward (Reverse) - explicit pattern
""")
for i in range(4):
    print("l(R(text))")
    l(R('text'))
    b()

print("""
Search Forward again - stored pattern
""")
print("l(1)")
l(1) # back to top
for i in range(4):
    print("l(F(''))")
    l(F(''))
    b()


print("""
search backward (Reverse) -  stored pattern
""")
for i in range(4):
    print("l(R(''))")
    l(R(''))
    b()
