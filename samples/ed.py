"""
ed.py - ed is the standard text editor.  For more explanation see ed.md.

"""

buffers = dict() # { bufname, a string : Buffer instance }

current = None # string, current buffer is  buffers[buf]

o = None # int, index of current line (. or dot) in current buffer

S = None # int, index of last line $ in current buffer.

class Buffer(object):
    """
    Text buffer for ed 
    """
    def __init__(self):
        """
        New text buffer
        """
        self.lines = list() # buffer text, list of strings
        self.dot = None # int, index into lines
        self.unsaved = False # True when buffer contains unsaved changes

def B(name):
    """
    Create a new Buffer and load the file name.  Print the number of
    lines read (0 when creating a new file). The new buffer, also
    titled name, becomes the current buffer.
    """
    global buffers, current, S, o
    buffers[name] = Buffer()
    # if file doesn't exist, that's OK, start new one
    try:
        fd = open(name, mode='r')
    except IOError: 
        fd = None
    # what about other errors than No such file - ?
    # should we distinguish various Errno? 
    if fd:
        buffers[name].lines = fd.readlines()
        fd.close()
    current = name # do this only if readlines succeeded
    if buffers[current].lines: # not empty
        nlines = len(buffers[current].lines)
        S = nlines - 1 # index of last line
        buffers[current].dot = S
        o = S
    else:
        nlines = 0
        # dot, o, S ?
    print '%s, %d lines' % (name, nlines)
