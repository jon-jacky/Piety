"""
storage_frame.py - Wrap functions in storage module to update display

"""

import storage as st
import frame

# Save a reference to each of these before we reassign them
stcreate = st.create
stselect = st.select
stdelete = st.delete

def create(bufname):
    stcreate(bufname) # not st.create - that will be reassigned
    frame.create(st.buf)

def select(bufname):
    stselect(bufname)
    frame.select(st.buf)

def delete(bufname):
    stdelete(bufname)
    frame.remove(st.delbuf, st.buf)

