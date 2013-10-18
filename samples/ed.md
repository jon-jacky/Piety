
ed
==

**ed** is a text editor in pure Python.  It can run as a standalone
program, but is intended to run within an interactive Python session.
It can run concurrently with other tasks in the same session under *piety*, 
a cooperative multitasking scheduler.

**ed** is a simple line-oriented editor that provides some of the
commands from the classic Unix editor, *ed*, augmented with commands
for managing multiple buffers and files from a later Unix editor, *sam*.

Unix *ed* is decribed in many books: *The Unix Programming
Environment* by Kernighan and Pike, *Software Tools* by Kernighan and
Plauger, etc.  Or just type *man ed* on any Unix-like system.

Here is a brief **ed** session in a Python session:

    >>> import ed  
    >>> ed.cmd() 
    :B 'test.txt'
    :a
    ed.cmd() enters ed command mode, with the : command  prompt.
    'B <name>' creates a new buffer and loads the named file (if there is one).
    'a' enters ed insert mode and appends the text after the current line.
    'w' writes the buffer contents back to the file
    'q' quits ed command mode.
    To quit ed insert mode, type a period by itself at the start of a line.
 .
    :w
    :q
    >>>

After the *q* command, all the editor buffers and other context
remain, so the editing session can be resumed at any time by typing
*ed.cmd()* again.

For every *ed* command there is an ordinary Python function, so you
can edit directly from the Python interpreter prompt.  The following
commands have the same effect as the preceding example:

    >>> import ed
    >>> ed.B('test.txt')
    >>> ed.a()
 ... enter text, quit by typing a period at the start of a line ...
    >>> ed.w()

Likewise, you can edit with Python commands not provided in *ed*, for
example any of the Python string or regular expression methods.

Commands
--------

The *ed commands currently supported are:

(to come)

Internals
---------
