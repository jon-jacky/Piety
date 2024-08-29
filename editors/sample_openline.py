"""
sample_openline.py - Code fragments from sked.py, to edit for pmacs_openline demo.

"""

# First, edit these sections near the top of this file before the ######... line
#  to show the old openline behavior without automatic indentation.

try:
    _ = dot
except:
    # Code block with one level of indentation for testing openline
    buffer = ['\n']
    # ... Add more indented lines here ...

# ... many lines omitted ...

def w(fname=None, set_saved=set_saved):
    # Indented comment block for testing wrap 
    """
    w(rite) buffer to file, default fname is in filename.
    If fname is given, assign it to filename to be used for future writes.
    """
    global filename, bufname, saved
    # .. lines omitted ...
    if success:
        if filename != fname: # we saved buffer with a new, different filename
            # Code block with three levels of indentation
            filename = fname
            # ... add more indented lines here ...
        # Code block out-dented from preceding block
        set_saved(True)
        # ... add more out-dented lines here ...

# Next, revise and reload the code in pmacs.py that defines openline behavior
#  to add automatic indentation.

##############################################################################

# Then, edit these sections after the the ##########... line
#  to show the new openline behavior with automatic indentation.

try:
    _ = dot
except:
    # Code block with one level of indentation for testing openline
    buffer = ['\n']
    # ... Add more indented lines here ...

# ... many lines omitted ...

def w(fname=None, set_saved=set_saved):
    # Indented comment block for testing wrap 
    """
    w(rite) buffer to file, default fname is in filename.
    If fname is given, assign it to filename to be used for future writes.
    """
    global filename, bufname, saved
    # .. lines omitted ...
    if success:
        if filename != fname: # we saved buffer with a new, different filename
            # Code block with three levels of indentation
            filename = fname
            # ... add more indented lines here ...
        # Code block out-dented from preceding block
        set_saved(True)
        # ... add more out-dented lines here ...

