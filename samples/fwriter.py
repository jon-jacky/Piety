"""
fwriter.py - write a file to demonstrate concurrency in Piety

Each call to fwriter.write() writes a single line to the end of a
file, then flushes the file so the line appears immediately.  Each
line has a sequence number and a timestamp.

Schedule calls to fwriter on a recurring event, such as a periodic
timeout.  View the growing file in a terminal window with tail -f.

Optional argv[1] is filename, default fwriter.txt
"""

import sys
import datetime

fname = 'fwriter.txt'
if len(sys.argv) > 1:
    fname = sys.argv[1]
print 'fwriter: file name %s' % fname
f = open(fname, 'w')

seqno = 0

def write():
    global seqno
    s = '%6d %s\n' % (seqno, datetime.datetime.now())
    f.write(s)
    f.flush()  # so line appears immediately
    seqno += 1
