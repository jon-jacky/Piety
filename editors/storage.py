"""
storage.py - Dictionary of text buffers indexed by string buffer names
             for use by ed.py and other text editors.
"""

import buffer, frame

# Data structures and variables. Initialize these with create_buf (below)
buf = None       # current buffer
previous = str() # name of previous buffer
current = str()  # name of current buffer
buffers = dict() # dict from buffer names (strings) to Buffer instances

# Display, default is no display.  
# edda startup assigns displaying = True and frame = frame
displaying = False
frame = None

# functions that update data structures

def create_buf(bufname):
    'Create buffer with given name. Replace any existing buffer with same name'
    global previous, current, buf
    buf = buffer.Buffer(bufname)
    buffers[bufname] = buf # replace buffers[bufname] if it already exists
    previous = current
    current = bufname
    if displaying:
        frame.create(buf)

def select_buf(bufname):
    'Make buffer with given name the current buffer'
    global previous, current, buf
    previous = current
    current = bufname
    buf = buffers[current]
    if displaying:
        frame.select(buf)

