"""
printer.py - print to various destinations to demonstrate interleaving
              concurrency.

Defines class Timestamp, with a method that returns a single line including
a name, sequence number, the current time.  The name is an __init__ arg,
and the seqno starts at 0 and advances each time the method is called.

Multiple Timestamp instances can run concurrently, with the output of
each printed to its own destination.
"""

import sys, datetime
from timestamp import timestamp # generator

# For test

class Buffer(object):
    'stand-in for an ed0 text buffer'
    def __init__(self):
        self.lines = [] # buffer contents
        self.contents = ''
        self.end_phase = False # assumes first write is *not* the end string

    # Invoked by print(s, file=buffer), writes s to buffer
    # Experiments show that this Python print calls Buffer write *twice*,
    # first write for the contents s, second write for end string
    # even when end string is default \n or empty ''     
    # So here we alternate reading contents and discarding end string
    def write(self, s):
        #print([c for c in s]) # DEBUG reveals second write for end string
        #print('end_phase %s' % self.end_phase) # DEBUG
        if self.end_phase:
            # ignore the end string, ed0 buffer lines must end with \n
            self.lines.append(self.contents) # already  includes final'\n'
        else:
            # store contents string until we get end string
            self.contents = s
        self.end_phase = not self.end_phase # False True False ...


# Test

ts0, ts1 = timestamp('ts0'), timestamp('ts1')
buf0, buf1 = Buffer(), Buffer()

def main():
    print('Two generators interleaving, each printing five lines to stdout')
    for i in range(5):
        print(ts0.__next__()) # no file=... print to stdout
        print(ts1.__next__())
    print("""Two generators interleaving, each printing five lines to different buffer
 then print each buffer in turn""")
    # first print to both buffers
    for i in range(5):
        print(ts0.__next__(), file=buf0) # use file=... print to buffer
        print(ts1.__next__(), file=buf1)
    # then print contents of each buffer
    for line in buf0.lines:
        print(line.rstrip()) # buffer contents already include final \n
    for line in buf1.lines:
        print(line.rstrip()) 

if __name__ == '__main__':
    main()
