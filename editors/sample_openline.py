"""
sample_openline.py - Fragments from sked.py, to edit for pmacs.py open_line demo.

"""

# First, edit these sections near the top of this file before the ######... line
#  to show the old openline behavior without automatic indentation.

try:
    _ = dot
except:
    # Code block with one level of indentation for testing openline
    buffer = ['\n']
    # Add more indented lines here.  You can copy them from the real sked.py.
    # You have to type the tab key, or type the space key four times,
    #  to reach the required indentation.

# ... many lines omitted ...

def w(fname=None, set_saved=set_saved):
    # Indented comment block for testing wrap.
    # Add line in the middle, then select the three command lines
    #  and wrap with M-q.  The wrapped lines start at the left margin of 
    #  the window, which looks terrible.
    """
    w(rite) buffer to file, default fname is in filename.
    ... more comment text follows ...
    """
    global filename, bufname, saved
    # .. lines omitted ...
    if success:
        if filename != fname: # we saved buffer with a new, different filename
            # Code block with three levels of indentation
            filename = fname
            # Add more indented lines here.  You have to type tab three times,
            # or type 12 spaces, to reach the required indentation.            

        # Code block out-dented from preceding block
        set_saved(True)
        # Add more out-dented lines here. You have to type tab two times 
        #  or type eight spaces to reach the required indentation. 
         
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
    # Add more indented lines here.  You can copy them from the real sked.py.
    # You have to type the tab key, or type the space key four times,
    #  to reach the required indentation.

# ... many lines omitted ...

def w(fname=None, set_saved=set_saved):
    # Indented comment block for testing wrap.
    # Add line in the middle, then select the three command lines
    #  and wrap with M-q.  The wrapped lines start at the left margin of 
    #  the window, which looks terrible.
    """
    w(rite) buffer to file, default fname is in filename.
    ... more comment text follows ...
    """
    global filename, bufname, saved
    # .. lines omitted ...
    if success:
        if filename != fname: # we saved buffer with a new, different filename
            # Code block with three levels of indentation
            filename = fname
            # Add more indented lines here.  You have to type tab three times,
            # or type 12 spaces, to reach the required indentation.            

        # Code block out-dented from preceding block
        set_saved(True)
        # Add more out-dented lines here. You have to type tab two times 
        #  or type eight spaces to reach the required indentation. 

