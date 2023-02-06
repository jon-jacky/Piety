"""
skedinit - Define and initialize global variables used by editor functions
           in the sked module: text buffer, current location, etc.
"""

# buffer is zero indexed, but we want first line of file to be at index 1
# so first entry in buffer list is never used - it's always just '\n'
buffer = ['\n']  # '\n' at index 0 is never used
o = 0            # dot, index of current line in buffer.  o looks like ed .

filename = 'test.txt' # reassigned by e(dit) and w(rite) commands
searchstring = 'def ' # reassigned by s(earch) and r(everse) commands
pagesize = 12         # reassigned by v and mv page up/down commands
saved = True          # True when no unsaved changes, safe to run e(dit).

yank = [] # yank (paste) buffer
