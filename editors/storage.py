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

# Basic functions that update data structures: create, select, delete

def create(bufname):
    'Create buffer with given name. Replace any existing buffer with same name'
    global previous, current, buf
    buf = buffer.Buffer(bufname)
    buffers[bufname] = buf # replace buffers[bufname] if it already exists
    previous = current
    current = bufname
    if displaying:
        frame.create(buf)

def select(bufname):
    'Make buffer with given name the current buffer'
    global previous, current, buf
    previous = current
    current = bufname
    buf = buffers[current]
    if displaying:
        frame.select(buf)

def delete(bufname):
    'Delete buffer with given name, might be the current buffer'
    delbuf = buffers[bufname]
    del buffers[bufname]
    if bufname == current: # pick a new current buffer
        keys = list(buffers.keys()) # always nonempty due to main
        select(keys[0]) # reassigns current
        previous = current
    if displaying:
        frame.remove(delbuf, buf)

# Queries and predicates

def bufs_for_file(filename):
    'Return list of names of buffers editing filename, empty list if none'
    return [ buffers[b].name for b in buffers
             if buffers[b].filename == filename ]

def modified(bufname):
    'Return True if the named buffer is modified since last saved.'
    return (bufname in buffers and buffers[bufname].modified)

def any_modified():
    'Return True if any buffer is modified since last saved.'
    return any([buffers[b].modified for b in buffers])

def info(bufname):
    'Return a line of information about the named buffer.'
    return buffers[bufname].info()

def lines(bufname):
    'Return the list of lines in the named buffer.'
    return buffers[bufname].lines[1:] # lines[0] always empty

# Clients can use 'bufname in st.names()' instead of 'bufname in buffers'
# This hides buffers from client but is not less cluttered.

def names():
    'Return list of all the buffer names.'
    keys = buffers.keys() # returns a dict_keys object, not indexable
    return list(keys) 

