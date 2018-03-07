
etty
====

**etty.py** runs the *ed.py* line editor in a *Console* job to collect
  and edit input lines.  It demonstrates how to use non-default
  keymaps in a *Console* job to provide retro style editing and
  history, as would be provided by a printing terminal.  Contrast to
  the *ed.py* *main* function and *edda.py*.

A printing terminal has no cursor addressing --- the printing element
can only move forward from the end of the text.  So you can only
delete the character you typed last.  You can't actually remove the
deleted (but already printed) character (*c* for example) so *etty*
indicates deletes by printing *\c* when you delete *c*.  It is often
helpful to type *^L* to print the edited text on a new line, or *^U*
to start over on a new line.

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
