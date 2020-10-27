"""
textframe.py - wrap functions in ed.py and text.py, methods in buffer.py
                   with calls to frame.py to update display
"""

import frame, ed, buffer, text

# wrap functions in ed.py

# Save a reference to each of these before we reassign them.
# This is necessary to restore unwrapped fcns, also to break infinite recursion.
ed_l = ed.l
ed_p_lines = ed.p_lines
ed_prepare_input_mode = ed.prepare_input_mode
ed_set_command_mode = ed.set_command_mode

# define wrapped functions

# Assign displaying = True or False to turn display updates on or off.
displaying = False  # Initially, display does not update even when enabled
    
def prepare_input_mode(cmd_name, start, end):
    ed_prepare_input_mode(cmd_name, start, end) # not ed.prepare_input_mode
    if displaying: frame.input_mode()

def set_command_mode():
    ed_set_command_mode()
    if displaying: frame.command_mode()

# wrap functions in text

# Save a reference to each of these before we reassign them.
# This is necessary to restore unwrapped fcns, also to break infinite recursion.
text_create = text.create
text_select = text.select
text_delete = text.delete

# define the wrapped functions

def create(bufname):
    text_create(bufname)  # not text.create - that creates infinite recursion
    if displaying: frame.create(text.buf)

def select(bufname):
    text_select(bufname)
    if displaying: frame.select(text.buf)

def delete(bufname):
    text_delete(bufname)
    if displaying: frame.remove(text.delbuf, text.buf)

# wrap methods in buffer

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
        if displaying: frame.insert(iline, self.dot)          

    def insert_other(self, iline, lines):
        """
        Insert lines when this buffer is not the current buffer,
        for example when this buffer is updated by a background task.
        """
        super().insert_other(iline, lines)
        if displaying: frame.insert_other(self, iline, self.dot)

    def r(self, iline, filename):
        'Read file contents into buffer after iline.'
        file_found = super().r(iline, filename)
        if not file_found:
            if displaying: frame.select(self) # if file_found display already updated
        return file_found

    def w(self, name):
        'Write current buffer contents to file name.'
        super().w(name)
        if displaying: frame.status(self)

    def l(self, iline):
        'Advance dot to iline and return that line (so caller can print it)'
        line, prev_dot = super().l(iline)
        if displaying: frame.locate(prev_dot, iline)
        return line, prev_dot

    def d(self, start, end, yank=True):              
        'Delete text from start up through end'
        super().d(start, end, yank)
        if displaying: frame.delete(start, end)

    def I(self, start, end, indent):
        'Indent lines, add indent leading spaces'
        super().I(start, end, indent)
        if displaying: frame.mutate(start, end)

    def M(self, start, end, outdent):
        'Indent lines, add indent leading spaces'
        super().M(start, end, outdent)
        if displaying: frame.mutate(start, end)

    def s(self, start, end, old, new, glbl, use_regex):
        'Substitute new for old in lines from start up to end.'
        match = super().s(start, end, old, new, glbl, use_regex)
        if displaying: frame.mutate(start, self.dot) # self.dot is last line changed
        return match

    def u(self, iline):
        'Undo last substitution: replace line at iline from cut buffer'
        super().u(iline)
        if displaying: frame.mutate(iline, iline)

# Enable display updates by assigning wrapped functions and methods.

def enable():
    """
    Enable display updates by assigning wrapped functions and methods.
    Must assign displaying = True or False to turn display updates on or off.
    """
    ed.l = ed.l_noprint
    ed.p_lines = ed.p_lines_noprint
    ed.prepare_input_mode = prepare_input_mode
    ed.set_command_mode = set_command_mode
    text.create = create
    text.select = select
    text.delete = delete
    buffer.Buffer = BufferFrame

