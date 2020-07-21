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
import frame

def startup():
    # copied from ed.py top level
    st.create('main')  # initialize main buffer only once on import
    st.previous = 'main'

    # copied from edda.py top level
    frame.init(st.buf) 

    # copied from edda.py startup()
    frame.rescale(frame.cmd_h) # calls refresh, which calls set_scroll
    # Enable display in ed, buffer, storage modules. Defaults is no display.
    st.buffer.displaying = st.displaying = True
    st.buffer.frame = st.frame = frame

if __name__ == '__main__':
   startup()
   # exit to Python interpreter
