"""
storage_frame.py - Wrap functions in storage module to update display
"""

import storage as st
import frame

# Save a reference to each of these before we reassign them.
# This is necessary to restore unwrapped fcns, also to break infinite recursion.
st_create = st.create
st_select = st.select
st_delete = st.delete

# define the wrapped functions

def create(bufname):
    st_create(bufname)  # not st.create - that creates infinite recursion
    frame.create(st.buf)

def select(bufname):
    st_select(bufname)
    frame.select(st.buf)

def delete(bufname):
    st_delete(bufname)
    frame.remove(st.delbuf, st.buf)

# Enable/disable display by assigning/restoring wrapped/uwrapped fcns in st

def enable():
    'Enable display by assigning wrapped functions in storage'
    st.create = create
    st.select = select
    st.delete = delete

def disable():
    'Disable display by restoring unwrapped functions in storage'
    st.create = st_create
    st.select = st_select
    st.delete = st_delete

