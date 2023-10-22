"""
skedinit - Define and initialize global variables used by editor functions
           in the sked module: text buffer, current location, etc.
"""

# Buffer state is stored in several module-level variables, not an object
# because classes and objects do not play well with Python reload().

# buffer is zero indexed, but we want first line of file to be at index 1
# so first entry in buffer list is never used - it's always just '\n'
buffer = ['\n']  # '\n' at index 0 is never used
dot = 0            # dot, index of current line in buffer

filename = 'scratch.txt' # reassigned by e(dit) and w(rite) commands
bufname = filename  # Basename of filename, reassigned by e and w
searchstring = 'def ' # reassigned by s(earch), r(everse) and c(hange) commands
replacestring = '??? ' # reassigned by c(hange) command
pagesize = 12         # reassigned by v and mv page up/down commands
saved = True          # True when no unsaved changes, safe to run e(dit).
lmargin = 0           # left margin for wrap
rmargin = 78          # right margin for wrap
nindent = 4           # N of spaces to indent or outdent

killed = [] # yank (paste) buffer filled by kill_region or repeated kill_line

# saved buffers, dictionary from buffer names to dict of buffer items
# initialize so there is always a saved buffer to switch back to
buffers = dict()
buffers[bufname] = {'bufname': bufname, 'filename': filename, 
                    'buffer': buffer, 'dot': dot, 'saved': saved }

prev_bufname = bufname # so we can switch back even before we save any buffers
