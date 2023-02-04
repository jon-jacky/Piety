"""
skedinit - Define and initialize global variables used by editor
           functions in the sked module.

The variables defined and initialized here store the state of the sked
editor session: the text in the buffer, the location of the current
line 'dot', etc.  The statements here must be executed before calling
any of the functions in sked.

The sked editor functions are in a separate module so they can
be reloaded into an editor session after revising or adding functions,
without re-initializing these variables and losing data.
"""

# buffer is zero indexed, but we want first line of file to be at index 1
# so first entry in buffer list is never used - it's always just '\n'
buffer = ['\n']  # '\n' at index 0 is never used
o = 0            # dot, index of current line in buffer.  o looks like ed .

filename = 'main'     # default, reassigned by e command
searchstring = 'main' # default, reassigned by s(earch) and r(everse) commands
pagesize = 12         # default, reassigned by z command
