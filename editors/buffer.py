"""
buffer.py - Buffer class for line-oriented text editors.

In this buffer class, the text in the buffer is a list of strings
named 'lines'.  Each string in the list is a single line of text that
ends with '\n'.  The 'lines' list can be populated by calling the
standard Python file method 'readlines' on a text file.

Many of the methods in the Buffer class correspond to ed commands and
the ed.py API.  The API (method calls) here use the classic Unix ed
conventions for indexing and range (which are unlike Python): The
index of the first line is 1, the index of the last line is the same
as the number of lines (the length of the buffer in lines), and range
i,j includes the last line with index j (so the range i,i is just the
line i, but it is not empty).  The buffer attribute named 'dot' is the
index of the current line in the buffer, which is often used as the
text insertion point.

In this class each method has a fixed (positional) argument list,
provides no error checking, and no error messages or progress
messages.  This class has no print statements, and does not read or
write at the console.  This class only updates buffers and reads and
writes files.

This Buffer class provides a write method so other code can update
text buffers without using the ed.py user interface or API, simply
calling the standard Python print function, with the file=... optional
argument pointing to the buffer.
"""

import os.path
from enum import Enum
from updates import update, Op

class Buffer(object):
    'Text buffer for editors, a list of lines (strings) and state variables.'

    # assigned by d(elete) in current buffer, may be used by y(ank) in another
    deleted = list() # most recently deleted lines from any buffer, for yank
    deleted_mark = list() # markers for deleted lines, for yank command

    def __init__(self, name):
        'New text buffer'
        self.name = name
        # Buffer always contains empty line at index 0, never used or printed
        self.lines = [''] # text in current buffer, a list of strings
        self.dot = 0 # index of current line, 0 when buffer is empty
        self.filename = None # file name (string) to read/write buffer contents
        self.unsaved = False # True if buffer contains unsaved changes
        self.pattern = '' # search string - default '' matches any line
        self.npage = 22 # page length used, optionally set by z scroll command
        self.mark = dict() # dict from mark char to line num, for 'c addresses
        self.end_phase = False # control variable used by write method

    def empty(self):
        'True when buffer is empty (not couting empty line at index 0)'
        return self.dot == 0

    def info(self):
        'return string with unsaved flag, buffer name, size in lines, filename'
        return ((' * ' if self.unsaved else '   ') +  # reserve col 1 for readonly flag
                '%-15s' % self.name + '%7d' % self.S() + '  %s' % self.filename)

    # write method for other programs (besides editors) to write into buffers
    # The call print(s, file=buffer), invokes this method to write s to buffer
    # Experiments show that this Python print calls this write method twice,
    # first write for the contents s, second write for end string
    # even when end string is default \n or empty ''     
    # So here we alternate reading contents and discarding end string
    def write(self, s):
        'Invoked by print(s, file=buffer), writes s to buffer'
        #print([c for c in s]) # DEBUG reveals second write for end string
        #print('end_phase %s' % self.end_phase) # DEBUG
        if self.end_phase:
            # ignore the end string, buffer lines must end with \n
            # self.lines.append(self.contents) # already  includes final'\n'
            self.a(self.dot, self.contents) # append command, advances dot
        else:
            # store contents string until we get end string
            self.contents = s
        self.end_phase = not self.end_phase # alternates False True False ...

    # line addresses

    def S(self):
        'like ed $, Return index of the last line, 0 if the buffer is empty'
        return len(self.lines)-1 # don't count empty first line at index 0

    # search

    def search_buf(self, forward):
        """Search for self.pattern.  Search forward from .+1 to end of buffer
        (or if forward is False, search backward from .-1 to start of buffer)
        If found, return line number.  If not found, return None.
        This version stops at end (or start) of buffer, does not wrap around.
        This version searches for exact match, not regex match."""
        found = False
        slines = self.lines[self.dot+1:] if forward \
            else reversed(self.lines[:self.dot-1])
        for imatch, line in enumerate(slines):
            if self.pattern in line:
                found = True
                break
        if not found:
            return None
        return self.dot+1 + imatch if forward else self.dot-2 - imatch

    def search(self, pattern, forward):
        """Update self.pattern if pattern is nonempty, otherwise retain old pattern
        Search for self.pattern, return line number where found, dot if not found
        Search forward if forward is True, backward otherwise."""
        if pattern:
            self.pattern = pattern 
        imatch = self.search_buf(forward)
        return imatch if imatch else self.dot

    def F(self, pattern):
        """Forward Search for pattern, 
        return line number where found, dot if not found"""
        return self.search(pattern, True)

    def R(self, pattern):
        """Backward search for pattern, 
        return line number where found, self.dot if not found"""
        return self.search(pattern, False)

    # helpers for r(ead), a(ppend), i(nsert), c(hange) etc.

    def insert(self, iline, lines, origin=0): 
        """Insert lines (list of strings) before iline,
        update dot to last inserted line"""
        self.lines[iline:iline] = lines # sic, insert lines at this position
        nlines = len(lines)
        self.dot = iline + nlines - 1
        self.unsaved = True # usually the right thing but ed.B .E override it.
        # adjust line numbers for marks below the insertion point
        for c in self.mark:
            if self.mark[c] >= iline:
                self.mark[c] += nlines
        # start and end of inserted text, end == destination == dot
        update(Op.insert, buffer=self, origin=origin, destination=self.dot,
               start=iline, end=self.dot)

    # files

    def f(self, filename):
        'set default filename for current buffer'
        self.filename = filename

    def r(self, iline, filename):
        'Read file contents into buffer after iline'
        if os.path.isfile(filename): 
            strings = [] # in case readlines fails
            with open(filename, mode='r') as fd:
                # fd.readlines reads file into a list of strings, one per line
                strings = fd.readlines() # each string in lines ends with \n
            self.insert(iline+1, strings) # like append, below

    def w(self, name):
        'Write current buffer contents to file name'
        with open(name, 'w') as fd:
            for line in self.lines[1:]: # don't print empty line 0
                fd.write(line)
        self.unsaved = False

    # displaying and navigating text

    def l(self, iline):
        'Advance dot to iline and return it (so caller can print it)'
        prev_dot = self.dot
        self.dot = iline
        update(Op.locate, buffer=self, origin=prev_dot, destination=iline)
        return (self.lines[iline]).rstrip() # strip trailing \n

    # adding, changing, and deleting text

    def a(self, iline, string):
        'Append lines from string after iline, update dot to last appended line'
        # string is one big str with linebreaks indicated by embedded \n
        # splitlines(True) breaks at \n to make list of strings
        # keepends True arg keeps each trailing \n, same convntn as fd.readlines()
        self.insert(iline+1, string.splitlines(True))

    def i(self, iline, string):
        'Insert lines from string before iline, update dot to last inserted line'
        # iline at initial empty line with index 0 is a special case, must append
        self.insert(iline if iline else iline+1, string.splitlines(True))

    def d(self, start, end):
        'Delete text from start up through end.'
        Buffer.deleted = self.lines[start:end+1] # save deleted lines for yank
        self.lines[start:end+1] = [] # ed range is inclusive, unlike Python
        self.unsaved = True
        if self.lines[1:]: # retain empty line 0
            # first line after deletes, or last line in buffer
            self.dot = min(start,self.S()) # S() if we deleted end of buffer
        else:
            self.dot = 0
        # new_mark needed because we can't remove items from dict as we iterate
        new_mark = dict() #new_mark is self.mark without marks at deleted lines
        Buffer.deleted_mark = dict() 
        for c in self.mark: 
            if (start <= self.mark[c] <= end): # save marks from deleted lines
                Buffer.deleted_mark[c] = self.mark[c]-start+1
            else:
                # adjust marks below deleted lines
                markc = self.mark[c]
                new_mark[c] = markc - self.nlines if markc >= end else markc
        self.mark = new_mark
        # origin, start, end are before deletion
        # destination == dot after deletion, first line following deleted lines
        update(Op.delete, buffer=self, origin=start, destination=self.dot,
               start=start, end=end) # destination?

    def c(self, start, end, string):
        'Change (replace) lines from start up to end with lines from string.'
        # ed (and also edsel) call d(elete) when command is 'c'
        # then handle new lines as later a(ppend) commands ...
        self.d(start,end)
        # ...but API c method does handle string argument.  
        self.i(start,string) # This i calls string.splitlines(True)

    def s(self, start, end, old, new, glbl):
        """Substitute new for old in lines from start up to end.
        When glbl is True, substitute all occurrences in each line,
        otherwise substitute only the first occurrence in each line."""
        for i in range(start,end+1): # ed range is inclusive, unlike Python
            if old in self.lines[i]: # test to see if we should advance dot
                self.lines[i] = self.lines[i].replace(old,new, -1 if glbl else 1)
                self.dot = i
                self.unsaved = True
        update(Op.mutate, buffer=self, start=start, end=end) # destination?

    def y(self, iline):
        'Insert most recently deleted lines before iline.'
        # based on def i ... above
        self.insert(iline if iline > 0 else iline+1, Buffer.deleted)
        # restore marks, if any
        for c in Buffer.deleted_mark:
            if c not in self.mark: # do not replace existing marks
                self.mark[c] = Buffer.deleted_mark[c]+iline-1

    def t(self, start, end, dest):
        'Transfer (copy) lines to after destination line.'
        self.insert(dest+1, self.lines[start:end+1], origin=start) 

    def m(self, start, end, dest):
        'Move lines to after destination line.'
        self.d(start, end)
        nlines = (end-start) + 1
        # start, end refer to origin *before* move
        # now dest must be adjusted to refer to destination *after* move
        dest = (dest+1) - nlines if start < dest else dest+1 
        self.y(dest) # d then y maintain self.mark
