"""
printer.py - print to various destinations to demonstrate interleaving
              concurrency.

Defines class Printer, with a method that prints a single line on any
object that provides a write method.

By default, this line contains sequence number, name, timestamp.  A different
function to generate the line in some other form can be passed as an
optional argument to the constructor.

Multiple Printer instances can run concurrently, with the output of
each written to its own destination.
"""

import sys, datetime

class Printer(object):
    """
    Print to demonstrate interleaving concurrency, see module header
    """
    def __init__(self, destination=sys.stdout, name='main.txt', makeline=None):
        """ 
        Creates a Printer instance.  All argument are keyword args with defaults.
        destination - object to print on, default prints on stdout
        name - string passed to makeline function (next arg), default main.txt
        makeline - function that returns line to print, takes two required args
                    seqno and name.  Default also generates a timestamp.
        """
        self.destination = destination
        self.seqno = 0
        self.name = name
        self.makeline = makeline if makeline else self.default_makeline
        
    def default_makeline(self, seqno, name):
        """ 
        returns a line with sequence number, name, and also timestamp:
         5 main.txt 2013-07-13 11:32:42.231009
        """
        # no trailing \n, print adds that by default
        return '%6d %s %s' % (seqno, name, datetime.datetime.now())

    def print(self):
        'print single line to the destination, increment sequence number'
        # Buffer requires final \n, but we can't add it with default print end=
        s = self.makeline(self.seqno, self.name) + '\n'
        print(s, file=self.destination, end='')
        self.seqno += 1

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

pr0, pr1 = Printer(name='pr0'), Printer(name='pr1')

buf0, buf1 = Buffer(), Buffer()
prbuf0 = Printer(destination=buf0, name='prbuf0')
prbuf1 = Printer(destination=buf1, name='prbuf1')

def main():
    print("""Two printers interleaving, each printing five lines to stdout
""")
    for i in range(5):
        pr0.print()
        pr1.print()
    print("""
Two printers interleaving, each printing five lines to different buffer
 then print each buffer in turn
""")
    for i in range(5):
        prbuf0.print()
        prbuf1.print()
    for line in buf0.lines:
        print(line.rstrip()) # buffer contents already include final \n
    print()
    for line in buf1.lines:
        print(line.rstrip()) 

if __name__ == '__main__':
    main()
