"""
skedinit - Define and initialize global variables used by editor functions
           in the sked module: text buffer, current location, etc.
"""

# Buffer state is stored in several module-level variables, not an object
# because classes and objects do not play well with Python reload().

# buffer is zero indexed, but we want first line of file to be at index 1
# so first entry in buffer list is never used - it's always just '\n'
buffer = ['\n']  # '\n' at index 0 is never used
o = 0            # dot, index of current line in buffer.  o looks like ed .

filename = 'test.txt' # reassigned by e(dit) and w(rite) commands
bufname = 'test.txt'  # Basename of filename, reassigned by e and w
searchstring = 'def ' # reassigned by s(earch) and r(everse) commands
pagesize = 12         # reassigned by v and mv page up/down commands
saved = True          # True when no unsaved changes, safe to run e(dit).

yank = [] # yank (paste) buffer

buffers = {} # saved buffers, dictionary from names to tuples of buffer state

prev_bufname = 'test.txt' # so we can easily switch back.
