
etty
====

**etty.py** runs the *ed.py* line editor in a *Console*
  job to collect and edit input lines.  Uses
  non-default keymaps with the *Console* class to provide retro
  printing-terminal-style editing and history.  Contrast to *ed.py*
  *main* function and *edda*.

Here is a sample session started from the command line:

    ...$ python3 -m etty
    :a 
    Here is  \ a line of tet\txt
    Her \ e is another ^L
    Here is another \ ^L
    Here is another
    ,\,.
    :,p
    Here is a line of text
    Here is another
    :q
    ...$

Here is a sample session started in Python.

    ...$ python3
    ...
    >>> from etty import *
    >>> etty('lines20.txt',p='')
    lines20.txt, 20 lines
    a
    Her is a ^U
    Here is a line of text.
    Here is another lie\\\\ene^L
    Here is another line.
    .
    q
    ...$

Revised March 2018