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

class Timestamp(object):
    """
    Has a makeline method that returns a single line including
     a sequence number, label, and the current time.  
    The sequence number starts at 0 and advances on each call to makeline
    The label is an __init__ arg
    """

    def __init__(self, label='main.txt'):
        'label - string printed in every line, default main.txt'
        self.seqno = 0
        self.label = label

    def makeline(self):
        """ 
        returns a line with sequence number, label, and also timestamp:
         5 main.txt 2013-07-13 11:32:42.231009
        """
        # no trailing \n, print adds that by default
        s =  '%6d %s %s' % (self.seqno, self.label, datetime.datetime.now())
        self.seqno += 1
        return s

# For test

class Buffer(object):
    'stand-in for an ed0 text buffer'
    def __init__(self):
        self.lines = [] # buffer contents
        # For processing writes to buffer via Python print(s, file=buffer)
        # Experiments show that this Python print calls Buffer write *twice*,
        # first write for the contents s, second write for end string
        # even when end string is default \n or empty ''     
        # So here we alternate reading contents and discarding end string
        self.contents = ''
        self.end_phase = 0  # assumes first write is *not* the end string

    # Invoked by print(s, file=buffer)
    def write(self, s):
        #print([c for c in s]) # DEBUG reveals second write for end string
        #print('end_phase %s' % self.end_phase) # DEBUG
        if self.end_phase:
            # ignore the end string, ed0 buffer lines must end with \n
            self.lines.append(self.contents) # already  includes final'\n'
        else:
            # store contents string until we get end string
            self.contents = s
        self.end_phase = 0 if self.end_phase else 1 # 0 1 0 1 ...


# Test

ts0, ts1 = Timestamp(label='ts0'), Timestamp(label='ts1')

buf0, buf1 = Buffer(), Buffer()

def main():
    print('Two printers interleaving, each printing five lines to stdout')
    for i in range(5):
        print(ts0.makeline()) # no file=... print to stdout
        print(ts1.makeline())
    print("""Two printers interleaving, each printing five lines to different buffer
 then print each buffer in turn""")
    # first print to both buffers
    for i in range(5):
        print(ts0.makeline(), file=buf0) # use file=... print to buffer
        print(ts1.makeline(), file=buf1)
    # then print contents of each buffer
    for line in buf0.lines:
        print(line.rstrip()) # buffer contents already include final \n
    for line in buf1.lines:
        print(line.rstrip()) 

if __name__ == '__main__':
    main()
