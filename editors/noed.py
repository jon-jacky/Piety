""" 
noed.py - Pronounced "no ed".  Multi-buffer display editor with no
  command language or input other than the Python interpreter.

Demonstrates that the text and display modules do not depend on any
application.  All the functions and methods in the text, frame, textframe,
buffer and window modules are available.  You can print directly to text buffers.

Here is a sample session:

...$ python -im noed

... window into empty main buffer appears ...

>>> text.buf.a(0, 'Here is a line of text') # append after line 0, at the top
>>> text.buf.a(1, 'and another')            # append after line 1
>>> print('Here is a third line', file=text.buf) # you can just print to a buffer
>>> frame.restore()                       # restore full-screen scrolling
>>> ^D

...$

"""

import text, frame, textframe

textframe.enable() # enable display updates

def startup():
    # based on edda startup and ed startup
    cmd_h = 2
    text.startup('main') # initialize text.buf with main buffer
    textframe.displaying = True # turn on display updates
    frame.startup(cmd_h, text.buf) # create initial window into buf, refresh

if __name__ == '__main__':
   startup()
   # exit to Python interpreter
