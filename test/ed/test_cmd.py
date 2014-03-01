"""
test_cmd - utility function for testing ed.py

"""

from ed import *

def test_cmd(f, descrip, *args):
    print '> %s%s # %s' % (f.__name__, args, descrip)
    f(*args) if args != ((),) else f() # empty args special case
    print "> e() # print buffer status"
    e()
    if buf().lines:
        print "> p() # print the current line"
        p()
    saved_dot = o() # save dot because...

    # print the entire buffer leaves dot at the last line
    print "> p(1,S())   # print the entire buffer"
    p(1,S())
    print
    buf().dot = saved_dot # put it back where it was, undo effect of p(...)

