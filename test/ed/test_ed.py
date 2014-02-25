"""
test_ed.py  - test, demonstrate Python API for the text editor ed.py

 python -i test_ed.py

Remove test_ed.txt before running this script again, to obtain the same results

ed functions tested in this version: B n m p l o S b D i a w d

"""

from ed import *

# B() TypeError: B() takes exactly 1 argument (0 given)
# B('test.txt')

print "> B(42) # filename expected, print error message"
B(42)
print
print "> B('test_ed.txt') # read new file"
B('test_ed.txt')
print
print "> B('ed.py.txt') # read existing file"
B('ed.py.txt')
print
print "> n() # list all buffers"
n()
print
print "> e() # describe current buffer"
e()
print

print "> p(0,6) # print lines 0 up to (not including) 6"
p(0,6)
print
print "> l(6) # set . to line 6 and print"
l(6)

print "> l() # advance . one line and print (several times)"
l()
l()
l()
l()
print
print "> p()    # print current line"
p()  
print
print "> p(99)  # print line 99, advance ."
p(99)
print
print "> p() # print current line"
p()
print
print "> print o()    # current line index"
print o()
print
print "> print S()    # length of buffer, last line index + 1"
print S()
print
print "> e()          # current buffer status"
e()
print

print "> n() # all buffers"
n()
print

print
print "> b('test_ed.txt') # set current buffer"
b('test_ed.txt')
print 
print "> e() # current buffer"
e()
print
print "> n() # all buffers"
n()
print

print "> D('foo.txt')  # buffer name expected, print error message"
D('foo.txt')
print

print "> D('ed.py.txt')  # Delete buffer"
D('ed.py.txt')
print

print "> n() # list all buffers"
n()
print

print '> i("""Line 1   # insert at the beginning of the buffer'
print '...'
i("""Line 1  
Line 2
Line 3""")
print "> p() # print the current line"
p()
print "> p(0,S()) # print the entire buffer"
p(0,S())
print 

print '> a("""Line A   # append at the end of the buffer'
print '...'
a("""Line A
Line B
Line C""")
print "> p() # print the current line"
p()
print "> p(0,S())   # print the entire buffer"
p(0,S())
print

print '> i(0, """Line a   # insert at the beginning of the buffer'
print '...'
i(0, """Line a
Line b
Line c""")
print "> p() # print the current line"
p()
print "> p(0,S())   # print the entire buffer"
p(0,S())
print


print '> l(3)  # move to the middle of the buffer'
l(3)
print '> i("""Line i   # insert in the middle of the buffer'
print '...'
i("""Line i
Line ii
Line iii""")
print "> p() # print the current line"
p()
print "> p(0,S())   # print the entire buffer"
p(0,S())
print

print '> a(5, """Line I   # append in the middle of the buffer'
print '...'
a(5, """Line I
Line II
Line III""")
print "> p() # print the current line"
p()
print "> p(0,S())   # print the entire buffer"
p(0,S())
print

print "> w()  # write file"
w()
print

print "> l(12) # go to line 12 and print"
l(12)
print

print "> p() # print current line"
p()
print

print "> d() # delete dot"
d()
print

print "> p() # print current line"
p()
print

print "> d(o(),S()) # delete current line through the end"
d(o(),S())
print

print "> p() # print current line"
p()
print

print "> p(0,S()) # print entire buffer"
p(0,S())
print

print '# Remove test_ed.txt before running this script again, to obtain the same result'
print
