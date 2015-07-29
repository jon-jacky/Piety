"""
timestamp generator 

Each call to a timestamp generator yields a single line including
a name, sequence number, the current time.  The name is the argument,
and the seqno starts at 0 and advances each time the method is called.

Multiple timestamp generators can run concurrently.

Based on Timestamp class in printer.py
"""

import datetime

def timestamp(label, n=0):
    """ 
    yields  a line with sequence number, label, and also timestamp:
     5 main.txt 2013-07-13 11:32:42.231009
    then increments the sequence number
    n is number of iterations, default n=0 iterates forever
    """
    seqno = 0
    while (seqno < n) if n > 0 else True:
        # no trailing \n, print adds that by default
        yield '%6d %s %s' % (seqno, label, datetime.datetime.now())
        seqno += 1
