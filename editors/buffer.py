"""
buffer.py - Buffer class for line-oriented text editors.
            The text in each buffer is a list of strings.
"""

import os.path
from enum import Enum
import view
from updates import Op, background_task

# Hook for display updates from background tasks to restore cursor etc.
inputline = None  # default: no updates from background tasks,no restore needed

class Buffer(object):
    'Text buffer for editors, a list of lines (strings) and state variables.'

    # assigned by y(ank), that is copy, or d(elete) in current buffer, 
    # may be used by x (put, paste) in same or any other buffer
    cut_buffer = list() # most recently deleted (or "yanked") lines from any buffer
    cut_buffer_mark = dict() # markers for deleted lines, for yank command

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
                '%-15s' % self.name + '%7d' % self.nlines() + '  %s' % self.filename)

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
            # self.a(self.dot, self.contents) # append command, advances dot
            self.insert(self.nlines()+1, self.contents.splitlines(True), 
                        origin=background_task, 
                        column=(inputline.start_col + inputline.point 
                                if inputline else 0))
        else:
            # store contents string until we get end string
            self.contents = s
        self.end_phase = not self.end_phase # alternates False True False ...

    # line addresses

    def nlines(self):
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

    def insert(self, iline, lines, origin=0, column=1): 
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
        view.update(Op.insert, buffer=self, origin=origin, 
                      destination=self.dot, start=iline, end=self.dot, 
                      column=column)

    def replace(self, iline, line):
        'replace the line at iline with another single line'
        if iline == 0: # empty buffer
            self.a(iline, line)
        else:
            self.lines[iline] = line
        self.unsaved = True
        # No update needed when line is edited in place on screen

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
        else:
            view.update(Op.select, buffer=self) # new buffer for new file

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
        view.update(Op.locate, buffer=self,origin=prev_dot,destination=iline)
        return (self.lines[iline]).rstrip() # strip trailing \n

    # adding, changing, and deleting text

    def a(self, iline, string):
        'Append lines from string after iline,update dot to last appended line'
        # string is one big str with linebreaks indicated by embedded \n
        # splitlines(True) breaks at \n to make list of strings
        # keepends True arg keeps each trailing \n, same as with fd.readlines()
        self.insert(iline+1, string.splitlines(True), origin=iline)

    def i(self, iline, string):
        'Insert lines from string before iline, new dot is last inserted line'
        # iline at initial empty line w/ index 0 is a special case, must append
        self.insert(iline if iline else iline+1, string.splitlines(True),
                    origin=iline)

    def d(self, start, end):
        'Delete text from start up through end'
        self.y(start, end) # yank (copy, do not remove) lines to cut buffer
        self.lines[start:end+1] = [] # ed range is inclusive, unlike Python
        self.unsaved = True
        if self.lines[1:]: # retain empty line 0
            # first line after deletes, or last line in buffer
            self.dot = min(start,self.nlines()) # nlines() if we del end of buf
        else:
            self.dot = 0
        # new_mark needed because we can't remove items from dict as we iterate
        new_mark = dict() #new_mark is self.mark without marks at deleted lines
        Buffer.cut_buffer_mark = dict() 
        for c in self.mark: 
            if (start <= self.mark[c] <= end): # save marks from deleted lines
                Buffer.cut_buffer_mark[c] = self.mark[c]-start+1
            else:
                # adjust marks below deleted lines
                markc = self.mark[c]
                nlines = (end-start) + 1
                new_mark[c] = markc - nlines if markc >= end else markc
        self.mark = new_mark
        # origin, start, end are before deletion
        # destination == dot after deletion, first line following deleted lines
        view.update(Op.delete, buffer=self, 
                      origin=start, destination=self.dot, start=start, end=end)

    def c(self, start, end, string):
        'Change (replace) lines from start up to end with lines from string.'
        # ed (and also edsel) call d(elete) when command is 'c'
        # then handle new lines as later a(ppend) commands ...
        self.d(start,end)
        # ...but API c method does handle string argument.  
        self.i(start,string) # This i calls string.splitlines(True)

    def j(self, start, end):
        'Delete lines from start to end, replace with single line joined text'
        lines = [ line.rstrip() for line in self.lines[start:end+1] ]
        joined = ''.join(lines)+'\n'
        self.d(start, end)
        self.i(start, joined)

    def s(self, start, end, old, new, glbl):
        """Substitute new for old in lines from start up to end.
        When glbl is True, substitute all occurrences in each line,
        otherwise substitute only the first occurrence in each line."""
        origin = self.dot 
        for i in range(start,end+1): # ed range is inclusive, unlike Python
            if old in self.lines[i]: # test to see if we should advance dot
                self.y(i,i) # Cut buf only holds last line where subst, like GNU ed
                self.lines[i] = self.lines[i].replace(old,new, -1 if glbl 
                                                      else 1)
                self.dot = i
                self.unsaved = True
        # Update.end and .destination are last line actually changed
        view.update(Op.mutate, buffer=self, origin=origin,
                      start=start, end=self.dot, destination=self.dot)

    def y(self, start, end):
        'Yank (copy, do not remove) lines to cut buffer'
        Buffer.cut_buffer = self.lines[start:end+1]

    def x(self, iline):
        'Append (put, paste) cut buffer contents after iline.'
        self.insert(iline+1, Buffer.cut_buffer) # append
        # restore marks, if any
        for c in Buffer.cut_buffer_mark:
            if c not in self.mark: # do not replace existing marks
                self.mark[c] = Buffer.cut_buffer_mark[c]+iline

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
