"""
writer.py - write to files to demonstrate interleaving concurrency.

Defines class Writer, with a method that writes a single line to the
end of a file.  By default, this line contains the file name and a
timestamp.  A different function to generate the line in some other
form can be passed as an optional argument to the constructor.

Multiple Writer instances can run concurrently, with the output of
each displayed in its own window.
"""

import datetime

class Writer(object):
    """
    Write to files to demonstrate interleaving concurrency.

    The method write() writes a single line to the end of a file.
    Schedule calls to write() on a recurring event, such as a periodic
    timeout.  View the growing file in a terminal window with tail -f.
    Multiple Writer instances can run concurrently, with the output of
    each displayed in its own window.

    Each Writer instance includes a sequence number attribute,
    seqno, that counts the calls to its write().
    """

    fileno = 0 # used to generate default filenames

    def __init__(self, fname=None, makeline=None):
        """ 
        Creates a Writer instance and opens its file for writing.

        fname - optional argument, the name of the file to write.
        Otherwise Writer generates a unique name of the form
        file_N.txt, where N is a small decimal integer.  The file is
        opened in 'a' append mode (so opening the same name multiple
        times can make that file bigger, it doesn't start over).

        makeline - optional argument, the function to generate the
        line of text to write.  Otherwise Writer uses
        self.default_makeline defined here.
        """
        self.seqno = 0
        self.fname = fname if fname else 'file_%d.txt' % Writer.fileno
        self.makeline = makeline if makeline else self.default_makeline
        self.f = open(self.fname, 'a')
        Writer.fileno += 1
        
    def default_makeline(self, seqno, fname):
        """ 
        generates a line from the sequence number seqno, the filename
        fname, and also a new timestamp, for example:
        5 file_2.txt 2013-07-13 11:32:42.231009
        """
        return '%6d %s %s\n' % (seqno, fname, datetime.datetime.now())

    def write(self):
        """ writes a single line to the end of a file, flushes the file so the
        line appears immediately, increments the sequence number.
        """
        s = self.makeline(self.seqno, self.fname)
        self.f.write(s)
        self.f.flush()
        self.seqno += 1

    def close(self):
        """ closes the file
        """
        return self.f.close()
