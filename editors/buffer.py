"""
buffer.py - Buffer class for line-oriented text editors

In this buffer class, the text in the buffer is a list of strings
named 'lines' where each string in the list is a single line of text
in the buffer, and there is a current line named 'dot' which is the
text insertion point.

Many of the methods in the Buffer class correspond to ed commands
and the ed.py API.

The API (method calls) here use the classic Unix ed conventions for
indexing and range (which are unlike Python): The index of the first
line is 1, the index of the last line is the same as the number of
lines (the length of the buffer in lines), and range i,j includes the
last line with index j (so the range i,i is just the line i, but it is
not empty).

In this class each method has a fixed (positional) argument list,
provides no error checking, and no error messages or progress
messages.  This class has no print statements, and does not read or write at
the console.  This class only updates buffers and reads and writes files.

This Buffer class provides a write method so other code can update
text buffers without using the ed.py user interface or API, simply
calling the standard Python print function, with the file=... optional
argument pointing to the buffer.

The Buffer class has an attribute named update which can optionally be
assigned to a callable that may be used by the write method to update
a display (for example).
"""

import os.path

class Buffer(object):
    'Text buffer for editors, a list of lines (strings) and metadata'
    def __init__(self, name, update=None, caller=None):
        'New text buffer'
        self.name = name
        # Buffer always contains empty line at index 0, never used or printed
        self.lines = [''] # text in current buffer, a list of strings
        self.dot = 0 # index of current line, 0 when buffer is empty
        self.filename = None # filename (string) 
        self.unsaved = False # True if buffer contains unsaved changes
        self.pattern = '' # search string - default '' matches any line
        self.npage = 22 # page length used, optionally set by z scroll command
        self.end_phase = False # used by write method, see explanation below
        self.update = update # call from write method to update display
        # caller is the module which created this Buffer instance
        # used for referencing data that must be global to all buffers
        # for example the buffer of deleted text used by the yank command
        self.caller = caller 

    # line addresses

    def S(self):
        'like ed $, Return index of the last line, 0 if the buffer is empty'
        return len(self.lines)-1 # don't count empty first line at index 0

    # defaults and range checking, depend on indexing and range conventions

    def mk_start(self, start):
        'Return start if given, else default dot, 0 if buffer is empty'
        return start if start != None else self.dot

    def mk_range(self, start, end):
        """Return start, end if given, 
        else return defaults, calc default end from start"""
        istart = self.mk_start(start)
        return istart, end if end != None else istart

    def start_ok(self, iline):
        """Return True if iline address is in buffer, always False for empty buffer
        Used by most commands, which don't make sense for an empty buffer"""
        return (0 < iline <= self.S()) 

    def start_empty_ok(self, iline):
        """Return True if iline address is in buffer, or iline is 0 for start 
        Used by commands which make sense for an empty buffer: insert, append, read
        """
        return (0 <= iline <= self.S())

    def range_ok(self, start, end):
        'Return True if start and end are in buffer, and start does not follow end'
        return self.start_ok(start) and self.start_ok(end) and start <= end

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

    # helpers for r(ead), a(ppend), i(nsert), c(hange)

    def insert(self, iline, lines):
        """Insert lines (list of strings) before iline,
        update dot to last inserted line"""
        self.lines[iline:iline] = lines # sic, insert lines at this position
        self.dot = iline + len(lines)-1
        self.unsaved = True # usually the right thing but ed.B and E override it.

    # files

    def f(self, filename):
        'set default filename for current buffer'
        self.filename = filename

    def r(self, iline, filename):
        'Read file contents into buffer after iline'
        if os.path.isfile(filename): 
            fd = open(filename, mode='r')        
            # fd.readlines reads file into a list of strings, one per line
            strings = fd.readlines() # each string in lines ends with \n
            fd.close()
            self.insert(iline+1, strings) # like append, below

    def w(self, name):
        'Write current buffer contents to file name'
        fd = open(name, 'w')
        for line in self.lines[1:]: # don't print empty line 0
            fd.write(line)
        self.unsaved = False

    # displaying and navigating text

    def l(self, iline):
        'Advance dot to iline and return it (so caller can print it)'
        self.dot = iline
        return (self.lines[iline]).rstrip() # strip trailing \n

    # adding, changing, and deleting text

    def a(self, iline, string):
        'Append lines from string after iline, update dot to last appended line'
        # string is one big str with linebreaks indicated by embedded \n
        # splitlines(True) breaks at \n to make list of strings
        # keepends True arg keeps each trailing \n, same conventn as fd.readlines()
        self.insert(iline+1, string.splitlines(True))

    def i(self, iline, string):
        'Insert lines from string before iline, update dot to last inserted line'
        # iline at initial empty line with index 0 is a special case, must append
        self.insert(iline if iline else iline+1, string.splitlines(True))

    def d(self, start, end):
        """Delete text from start up to end, 
        set dot to first line after deletes or last line in buffer"""
        self.caller.deleted = self.lines[start:end+1] # save deleted lines for yank later
        self.lines[start:end+1] = [] # classic ed range is inclusive, unlike Python
        self.unsaved = True
        if self.lines[1:]: # retain empty line 0
            # first line after deletes, or last line in buffer
            self.dot = min(start,self.S()) # S() if we deleted end of buffer
        else:
            self.dot = 0

    def c(self, start, end, string):
        'Change (replace) lines from start up to end with lines from string'
        self.d(start,end)
        self.i(start,string) # original start is now insertion point

    def s(self, start, end, old, new, glbl):
        """Substitute new for old in lines from start up to end.
        When glbl is True, substitute all occurrences in each line,
        otherwise substitute only the first occurrence in each line."""
        for i in range(start,end+1): # classic ed range is inclusive, unlike Python
            if old in self.lines[i]: # test to see if we should advance dot
                self.lines[i] = self.lines[i].replace(old,new, -1 if glbl else 1)
                self.dot = i
                self.unsaved = True

    # Invoked by print(s, file=buffer), writes s to buffer
    # Experiments show that this Python print calls Buffer write *twice*,
    # first write for the contents s, second write for end string
    # even when end string is default \n or empty ''     
    # So here we alternate reading contents and discarding end string
    def write(self, s):
        'Invoked by print(s, file=buffer), writes s to buffer'
        #print([c for c in s]) # DEBUG reveals second write for end string
        #print('end_phase %s' % self.end_phase) # DEBUG
        if self.end_phase:
            # ignore the end string, ed0 buffer lines must end with \n
            # self.lines.append(self.contents) # already  includes final'\n'
            self.a(self.dot, self.contents) # append command, advances dot
        else:
            # store contents string until we get end string
            self.contents = s
        self.end_phase = not self.end_phase # alternates False True False ...
        if self.update:
            self.update()

    def y(self, iline):
        'Insert most recently deleted lines before iline, update dot to last inserted line'
        # based on def i ... above
        # iline at initial empty line with index 0 is a special case, must append
        self.insert(iline if iline else iline+1, self.caller.deleted)
        # FIXME - how to append at end of buffer?
