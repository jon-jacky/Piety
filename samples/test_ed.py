"""
test_ed.py  - test, demonstrate Python API for the text editor ed.py

Run this script from the directory above Piety, it uses relative paths:

 python -i Piety/samples/test_ed.py

ed functions tested in this version: B n m p l o S b D i a w

"""

from ed import *

# B() TypeError: B() takes exactly 1 argument (0 given)
# B('test.txt')

print "> B(42) # filename expected, print error message"
B(42)
print
print "> B('new.txt') # read new file"
B('new.txt')
print
print "> B('Piety/samples/ed.py') # read existing file"
B('Piety/samples/ed.py')
print
print "> n() # list all buffers"
n()
print
print "> m() # describe current buffer"
m()
print

print "> p(0,5) # print lines 0..5"
p(0,5)
print
print "> l(6) # set . to line 6 and print"
l(6)

print "> l() # advance . one line and print (several times)"
l()
l()
l()
print
print "> p()    # print current line"
p()  
print
print "> p(99)  # print line 99, don't change ."
p(99)
print
print "> p() # print current line"
p()
print
print "> print o()    # current line index"
print o()
print
print "> print S()    # last line index"
print S()
print
print "> m()          # current buffer status"
m()
print

print "> n() # all buffers"
n()
print

print
print "> b('new.txt') # set current buffer"
b('new.txt')
print 
print "> m() # current buffer"
m()
print
print "> n() # all buffers"
n()
print

print "> D('foo.txt')  # buffer name expected, print error message"
D('foo.txt')
print

print "> D('ed.py')  # Delete buffer"
D('ed.py')
print

print "> n() # list all buffers"
n()
print

print '> i("""Line 1   # insert at the beginning of the buffer'
print '...'
i("""Line 1  
Line 2
Line 3""")
print "> p(0,S()) # print the entire buffer"
p(0,S())
print 

print '> a("""Line A   # append at the end of the buffer'
print '...'
a("""Line A
Line B
Line C""")
print "> p(0,S())   # print the entire buffer"
p(0,S())
print

print '> i(0, """Line a   # insert at the beginning of the buffer'
print '...'
i(0, """Line a
Line b
Line c""")
print "> p(0,S())   # print the entire buffer"
p(0,S())
print


print '> l(4)  # move to the middle of the buffer'
l(4)
print '> i("""Line i   # insert in the middle of the buffer'
print '...'
i("""Line i
Line ii
Line iii""")
print "> p(0,S())   # print the entire buffer"
p(0,S())
print

print '> a("""Line I   # append in the middle of the buffer'
print '...'
a("""Line I
Line II
Line III""")
print "> p(0,S())   # print the entire buffer"
p(0,S())
print

print "> w()  # write file"
w()
print

print '# Remove new.txt before running this script again, to obtain the same results'
print



       
              
