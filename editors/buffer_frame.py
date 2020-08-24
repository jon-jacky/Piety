"""
buffer_frame.py - BufferFrame class derived from Buffer.
                  wrap Buffer methods that cause display updates.
"""

import buffer, frame

# Save a reference to the unwrapped base class before we reassign it.
# This is necessary to restore base class, also to break infinite recursion.
buffer_Buffer = buffer.Buffer

# define class with wrapped methods

class BufferFrame(buffer_Buffer):
    """
    BufferFrame class derived from Buffer
    wrap Buffer methods that cause display updates.
    """
      
    def __init__(self, name):
        super().__init__(name)

    def insert(self, iline, lines):
        'Insert lines before iline'
        super().insert(iline, lines)
        frame.insert(iline, self.dot)          

    def insert_other(self, iline, lines, column):
        """
        Insert lines when this buffer is not the current buffer,
        for example when this buffer is updated by a background task.
        """
        super().insert_other(iline, lines, column)
        frame.insert_other(self, iline, self.dot, column)          

    def r(self, iline, filename):
        'Read file contents into buffer after iline.'
        file_found = super().r(iline, filename)
        if not file_found:
            frame.select(self) # if file_found display already updated

    def w(self, name):
        'Write current buffer contents to file name.'
        super().w(name)
        frame.status(self)

    def l(self, iline):
        'Advance dot to iline and return that line (so caller can print it)'
        line, prev_dot = super().l(iline)
        frame.locate(prev_dot, iline)
        return line, prev_dot

    def d(self, start, end, yank=True):              
        'Delete text from start up through end'
        super().d(start, end, yank)
        frame.delete(start, end)

    def I(self, start, end, indent):
        'Indent lines, add indent leading spaces'
        super().I(start, end, indent)
        frame.mutate(start, end)

    def M(self, start, end, outdent):
        'Indent lines, add indent leading spaces'
        super().M(start, end, outdent)
        frame.mutate(start, end)

    def s(self, start, end, old, new, glbl, use_regex):
        'Substitute new for old in lines from start up to end.'
        super().s(start, end, old, new, glbl, use_regex)
        frame.mutate(start, self.dot) # self.dot is last line changed

    def u(self, iline):
        'Undo last substitution: replace line at iline from cut buffer'
        super().u(iline)
        frame.mutate(iline, iline)

# Enable/disable display by assigning/restoring wrapped/uwrapped buffer class 

def enable():
    'Enable display by assigning class with wrapped methods'
    buffer.Buffer = BufferFrame

def disable():
    'Disable display by reassigning base class'
    buffer.Buffer = buffer_Buffer

