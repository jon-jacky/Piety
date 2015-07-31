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


# Test

if __name__ == '__main__':

    print('Two bounded generators, one after the other, each printing five lines')
    for ts in timestamp('ts0', 5):
        print(ts)
    for ts in timestamp('ts1', 5):
        print(ts)

    print('Two infinite generators interleaving, each printing five lines')
    ts2, ts3 = timestamp('ts2'), timestamp('ts3')
    for i in range(5):
        print(next(ts2))
        print(next(ts3))

    """
    This doesn't work:

    print('Two bounded generators interleaving, each printing five lines')
    for t4,t5 in (timestamp('ts4', 5), timestamp('ts5', 5)):
        print(t4)
        print(t5)

    Traceback (most recent call last):
      File "timestamp.py", line 49, in <module>
        for t4,t5 in (timestamp('ts4', 5), timestamp('ts5', 5)):
    ValueError: too many values to unpack (expected 2)
    """
