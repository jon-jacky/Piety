"""
buffer.py - Buffer class for line-oriented text editors.
            The text in each buffer is a list of strings.
"""

import os.path, re, textwrap

# used by search methods
emptyline = '^\s*$'
no_match = -99  # must be same as no_match in check.py

class Buffer(object):
    'Text buffer for editors, a list of lines (strings) with state variables.'
    pattern = '' # search string - default '' matches any line
    # assigned by y(ank), that is copy, or d(elete) in current buffer,
    # may be used by x (put, paste) in same or any other buffer
    cut_buffer = list() # most recently deleted (or "yanked") lines from any buffer
    cut_buffer_mark = dict() # markers for deleted lines, for yank command
    # When yank_lines True, ^Y invokes edsel yank (paste lines)
    # when yank_lines False, ^Y invokes console yank (paste words inline) 
    yank_lines = True

    def __init__(self, name):
        'New text buffer'
        self.mode = 'Text' # other modes to come, maybe
        self.readonly = False
        self.name = name
        # Buffer always contains empty line at index 0, never used or printed
        self.lines = [''] # text in current buffer, a list of strings
        self.dot = 0 # index of current line, 0 when buffer is empty
        self.filename = None # file name (string) to read/write buffer contents
        self.modified = False # True if buffer contains unsaved changes
        self.mark = dict() # dict from mark char to line num, for 'c addresses
        self.end_phase = False # control variable used by write method
        self.fill_column = 75 # default, can be reassigned by J parameter
        self.found = False # True when search for Buffer.pattern succeeds

    def empty(self):
        'True when buffer is empty (not couting empty line at index 0)'
        return self.dot == 0

    def info(self):
        'return string with flags, name, size in lines, mode, filename'
        return (('%' if self.readonly else ' ') +
                ('*' if self.modified else ' ') +
                ' %-15s' % self.name + ' %7d' % self.nlines() +
                '  %-8s' % self.mode + 
                ' %s' % (self.filename if self.filename else '(no file)'))

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
            self.insert_other(self.nlines()+1, self.contents.splitlines(True))
        else:
            # store contents string until we get end string
            self.contents = s
        self.end_phase = not self.end_phase # alternates False True False ...

    # line addresses

    def nlines(self):
        'like ed $, Return index of the last line, 0 if the buffer is empty'
        return len(self.lines)-1 # don't count empty first line at index 0

    # search

    def match(self, pattern, iline):
        """
        pattern is regexp string (not compiled), iline is line number in buf.
        Return match object if pattern found in line, None otherwise.
        Named match, but uses re search not match to match anywhere in line.
        """
        return re.search(pattern, self.lines[iline])

    def lines_precede(self, iline):
        'returns True when more lines precede iline in buffer, False otherwise'
        return iline > 0    

    def lines_follow(self, iline):
        'returns True when more lines follow iline in buffer, False otherwise'
        return iline < self.nlines()   
    
    def search(self, pattern, direction, more_lines):
        """
        Regexp. search forward (backward) for pattern to end (start) of buffer.
        Return line number where pattern first found, return dot if not found.  
        If pattern arg is nonempty use it, otherwise use previous Buffer.pattern.
        pattern: regexp string (not compiled), unescaped meta chrs interpreted.
        direction: 1 forward toward end, -1 back toward start
        more_lines: True when more lines follow (precede) iline in buffer.
        """
        if pattern:
            Buffer.pattern = pattern
            self.found = False
        iline = self.dot + direction if more_lines(self.dot) else self.dot
        while not self.match(Buffer.pattern, iline) and more_lines(iline):
            iline += direction
        if self.match(Buffer.pattern, iline):
            self.found = True
            return iline
        else: 
            self.found = False
            return no_match
                     
    def F(self, pattern):
        """
        Regular expression search forward for string pattern.
        pattern: regexp string (not compiled), unescaped meta chrs interpreted.
        """
        return self.search(pattern, 1, self.lines_follow)

    def R(self, pattern):
        """
        Regular expression search backward for string pattern.
        pattern: regexp string (not compiled), unescaped meta chrs interpreted.
        """
        return self.search(pattern, -1, self.lines_precede)

    def para_edge(self, direction, more_lines):
        """
        A paragraph is a sequence of non-empty lines.
        Return number of first (last) line in paragraph that contains dot.
        If dot is on an empty line, return line nums from preceding paragraph.
        If no preceding paragraph, return 0.
        direction -1 to search back to first line, +1 search fwd to last line.
        more_lines: True when more lines precede (follow) iline in buffer.
        """
        iline = self.dot
        # If dot is empty line following paragraph, search back.
        # iline 0 is invisible empty line before visible line 1.
        while self.match(emptyline, iline) and iline > 0: 
            iline -= 1
        if iline == 0: # all lines in buffer are empty
            return 0   # invokes '? Invalid address'
        # Dot is non-empty line in paragraph, search back (forward) for empty.
        while not self.match(emptyline, iline) and more_lines(iline):
            iline += direction 
        # When searching forward, last line in buffer can be the edge
        if direction == 1 and not more_lines(iline):
            return iline
        else:
            return iline - direction # edge is line that follows (precedes) empty

    def para_first(self):
        'Return number of first line in paragraph that contains/precedes dot'
        return self.para_edge(-1, self.lines_precede)

    def para_last(self):
        'Return number of last line in paragraph that contains/precedes dot'
        return self.para_edge(1, self.lines_follow)

    # helpers for r(ead), a(ppend), i(nsert), c(hange) etc.

    # This method is called by both insert and insert_other, below
    # It separated out so we can display insert and insert_other differently.
    def insert_lines(self, iline, lines):
        """
        Insert lines (list of strings) before iline,
        update dot to last inserted line
        """
        self.lines[iline:iline] = lines # sic, insert lines at this position
        nlines = len(lines)
        self.dot = iline + nlines - 1
        self.modified = True # usually the right thing but ed.B .E override it.
        # adjust line numbers for marks below the insertion point
        for c in self.mark:
            if self.mark[c] >= iline:
                self.mark[c] += nlines

    def insert(self, iline, lines):
        """
        Insert lines when this buffer is the current buffer.
        If displaying, update the focus window via a wrapper in textframe or...
        """
        self.insert_lines(iline, lines)

    def insert_other(self, iline, lines):
        """
        Insert lines when this buffer is *not* the current buffer.
        If displaying, update other windows via wrapper but *not* focus window.
        """
        self.insert_lines(iline, lines)

    def replace(self, iline, line):
        'replace the line at iline with another single line'
        if self.empty(): # previously empty buffer, must create line
            self.a(iline, line) # sets modified True
            self.modified = not (line == '\n') # resets it on empty line only
        else:
            old_line  = self.lines[iline]
            self.lines[iline] = line
            if not (line == old_line):
                self.modified = True

    # files

    def f(self, filename):
        'set default filename for current buffer'
        self.filename = filename

    def r(self, iline, filename):
        """
        Read file contents into buffer after iline.
        Return file_found, False if not found, creating new file.
        """
        if os.path.isfile(filename):
            strings = [] # in case readlines fails
            with open(filename, mode='r') as fd:
                # fd.readlines reads file into a list of strings, one per line
                strings = fd.readlines() # each string in lines ends with \n
            self.insert(iline+1, strings) # like append, below
            file_found = True
        else:
            file_found = False
        return file_found

    def w(self, name):
        'Write current buffer contents to file name.'
        with open(name, 'w') as fd:
            for line in self.lines[1:]: # don't print empty line 0
                fd.write(line)
        self.modified = False

    # displaying and navigating text

    def l(self, iline):
        """
        Advance to iline and return that line (so caller can print it).
        Also return prev_dot, might be needed by display.
        """
        prev_dot = self.dot
        self.dot = iline
        line = (self.lines[iline]).rstrip('\n')
        return line, prev_dot

    # adding, changing, and deleting text

    def a(self, iline, string):
        'Append lines from string after iline,update dot to last appended line'
        # string is one big str with linebreaks indicated by embedded \n
        # splitlines(True) breaks at \n to make list of strings
        # keepends True arg keeps each trailing \n, same as with fd.readlines()
        self.insert(iline+1, string.splitlines(True))

    def i(self, iline, string):
        'Insert lines from string before iline, new dot is last inserted line'
        # iline at initial empty line w/ index 0 is a special case, must append
        self.insert(iline if iline else iline+1, string.splitlines(True))

    def d(self, start, end, yank=True):
        'Delete text from start up through end'
        if yank:
            self.y(start, end) # yank (copy, do not remove) lines to cut buffer
        self.lines[start:end+1] = [] # ed range is inclusive, unlike Python
        self.modified = True
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
        # start, end lines in buffer are before deletion
        # after deletion, win.buf.dot is first line following deleted lines
                      
    def c(self, start, end, string):
        'Change (replace) lines from start up to end with lines from string.'
        # ed (and also edda) call d(elete) when command is 'c'
        # then handle new lines as later a(ppend) commands ...
        self.d(start,end)
        # ...but API c method does handle string argument.  
        self.i(start,string) # This i calls string.splitlines(True)

    def j(self, start, end):
        'Delete lines from start to end, replace with single line joined text'
        lines = [ line.rstrip('\n') for line in self.lines[start:end+1] ]
        joined = ''.join(lines)+'\n'
        self.d(start, end, yank=False) # do not save joined lines in cut buffer
        self.i(start, joined)

    def J(self, start, end, fill_column):
        """
        Replace lines from start through end with wrapped (filled) lines.
        Left margin is first nonblank column in start line.
        Right margin is buf.fill_column, can be assigned by optional parameter.
        alternative algorithms to text.wrap:  http://xxyxyz.org/line-breaking/
        """
        if fill_column:
            self.fill_column = fill_column
        lines = self.lines[start:end+1]
        margin = ' ' * (len(lines[0]) - len(lines[0].lstrip()))
        filled = textwrap.fill(textwrap.dedent(''.join(lines)), 
                                width=self.fill_column-1,
                                initial_indent=margin, subsequent_indent=margin)
        self.d(start, end, yank=False)
        self.i(start, filled)

    def I(self, start, end, indent):
        'Indent lines, add indent leading spaces'
        self.lines[start:end+1] = [ ' '*indent + l for l in self.lines[start:end+1]]

    def M(self, start, end, outdent):
        'Outdent lines, remove leading outdent chars'
        self.lines[start:end+1] = [ l[outdent:] for l in self.lines[start:end+1]]

    def s(self, start, end, old, new, glbl, use_regex):
        """
        Substitute new for old in lines from start up to end.
        old, new treated as literal strings when use_regex is False,
        treated as regexp (string, not compiled) when use_regex  is True.
        When not regex and glbl True substitute all occurrences in each line,
        otherwise substitute only the first occurrence in each line.
        Return True if old found and substitution done, otherwise False
        """
        if not use_regex:
            old = re.escape(old)
        match = False
        for i in range(start,end+1): # ed range is inclusive, unlike Python
            if self.match(old, i):
                match = True
                self.y(i,i) # Cut buf only holds last line where subst, like GNU ed
                self.lines[i] = re.sub(old, new, self.lines[i])
                self.dot = i
                self.modified = True
        return match

    def y(self, start, end):
        'Yank (copy, do not remove) lines to cut buffer'
        Buffer.cut_buffer = self.lines[start:end+1]
        Buffer.yank_lines = True

    def u(self, iline):
        'Undo last substitution: replace line at iline from cut buffer'
        self.replace(iline, Buffer.cut_buffer[0])
        
    def x(self, iline):
        'Append (put, paste) cut buffer contents after iline.'
        self.insert(iline+1, Buffer.cut_buffer) # append
        # restore marks, if any
        for c in Buffer.cut_buffer_mark:
            if c not in self.mark: # do not replace existing marks
                self.mark[c] = Buffer.cut_buffer_mark[c]+iline

    def t(self, start, end, dest):
        'Transfer (copy) lines to after destination line.'
        self.insert(dest+1, self.lines[start:end+1]) # origin=start) 

    def m(self, start, end, dest):
        'Move lines to after destination line.'
        self.d(start, end)
        nlines = (end-start) + 1
        # start, end refer to origin *before* move
        # now dest must be adjusted to refer to destination *after* move
        dest = dest - nlines if start < dest else dest
        self.x(dest) # d then x maintain self.mark
