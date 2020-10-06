
text.py
=======

The *text* module manages text that persists through the Python
session. It provides a dictionary of text *Buffer* instances indexed by
buffer names (strings).   These text buffers are used by the *ed.py* and
*edsel* editors and other applications, but the *text* module does not
depend on any application and can by used by any.  The collection of
buffers is initialized by *text*, not by any application. Applications
can create, modify, and delete buffers by using functions and data in
*text*, but the collection of buffers persists unchanged when applications
start or exit.

Revised Oct 2020

