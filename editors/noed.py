""" 
noed.py - Pronounced "no ed".  Multi-buffer display editor with no
  command language or input other than the Python interpreter.

Demonstrates that the storage and display modules do not depend on any
application.

Here is a sample session:

...$ python -im noed

... window into empty main buffer appears ...

>>> st.buf.a(0, 'Here is a line of text') # append after line 0, at the top
>>> st.buf.a(1, 'and another')            # append after line 1
>>> frame.restore()                       # restore full-screen scrolling
>>> ^D

...$

"""

import storage as st
import frame, frame_wrapper

def startup():
    # based on edda startup and ed startup
    # Must be careful to intialize frame, enable buffers to update frame
    #  before initializing buffers
    cmd_h = 2
    frame_wrapper.startup(cmd_h) # enable display, must call before st.startup
    st.startup('main')
    frame.put_command_cursor() # st.startup leaves cursor on window status line

if __name__ == '__main__':
   startup()
   # exit to Python interpreter
