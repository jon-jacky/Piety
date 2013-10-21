
ed
==

**ed** is a text editor written in pure Python.  It can run as a
standalone program, but is intended to run in an interactive Python
session.  It has a Python API so you can edit from the Python prompt
or write editing scripts in Python.  It can run concurrently with
other tasks in the same session under *piety*, a cooperative
multitasking scheduler.  We anticipate using **ed** on a bare machine
running little more than a Python interpreter and the *piety*
scheduler.

**ed** is a line-oriented editor that provides some of the commands
from the classic Unix editor *ed*, augmented with commands for
managing multiple buffers and files from the later Unix (and Plan 9)
editor, *sam*.

Unix *ed* is decribed in many books: *The Unix Programming
Environment* by Kernighan and Pike, *Software Tools* by Kernighan and
Plauger, etc.  Or just type *man ed* on any Unix-like system.
The *sam* editor is described at [http://plan9.bell-labs.com/sys/doc/sam/sam.html](http://plan9.bell-labs.com/sys/doc/sam/sam.html).

Here is a brief **ed** session in a Python session:

    >>> from ed import *
    >>> ed()
    :B test.txt
    0 lines
    :a
    ed() enters ed command mode, with the : command  prompt.
    'B <name>' creates a new buffer and loads the named file
    'a' enters ed input mode and appends the text after the current line.
    'w' writes the buffer contents back to the file
    'q' quits ed command mode.
    To quit input mode, type a period by itself at the start of a line.
    .
    :w
    test.txt, 6 lines
    :q
    >>>

After the *q* command, all the editor buffers and other context
remain, so the editing session can be resumed at any time by typing
*ed()* again.

For every *ed* command there is an ordinary Python function, so you
can edit directly from the Python prompt.  The following
commands have the same effect as the preceding example:

    >>> from ed import *
    >>> B('test.txt')
    0 lines
    >>> a()
    ... enter text, quit by typing a period at the start of a line ...
    >>> w()
    test.txt, 6 lines

Likewise, you can edit in the buffers with Python commands not
provided in *ed*, for example with any of the string or regular
expression functions or methods.

### Python API ###

Here we describe the Python functions and attributes (variables) in
the *ed* module that implement editor commands.

Most functions have the same single-character names as the commands.

There may be several named text buffers, all stored in the variable
*buffers*, a dictionary from buffer names (strings) to buffer
instances.  Most commands apply to the *current buffer*, identified by
its name in the variable *current*.  The function call *buf()* returns
*buffers[current]*.  The contents of the current buffer are stored in
an array of lines (strings).  The function call *lines()* returns
*buf().lines*.

The current line (where, by default, text is changed or inserted) is
called *dot*.  After most commands, *dot* is updated to the last line
affected (the last line read in from a file, etc.).  The current line
*dot* and the last line in the buffer are identified by the variables
*o* and *S*, which look like . (period) and *$*, used in *ed* command
mode.  Our *o* and *S* are integer indices into the list of strings,
so *dot*, the current line, can be accessed as *lines()[o]*.

Many commands apply to a line *i* or to a range of lines starting with
*i* (included) up through line *j* (also included, unlike Python
slices).  Lines *i* and *j* can be identified by line number (an
integer index).  As usual for Python (but unlike Unix *ed*) 0
indicates the first line in the buffer.  The index -1 indicates the
last line in the buffer, and other negative numbers index backward
from the end (as usual for Python).  Line numbers can be represented
relative to *dot* or the last line, for example *o + 1* (the line
after *dot*) or *S - 3* (three lines before the last).

In each *ed* function call where they might appear, lines *i* and *j*
are always optional arguments in that order (declared with * *args*
syntax), with defaults (if used) assigned in the function body.
Usually *i* and *j* both default to *o* (*dot*), or *i, j* default to
*0, S* (beginning to end, the whole buffer).

Lines *i* and *j* can also be identified by the patterns (substrings)
they contain.  If you provide a string instead of a number for *i* or
*j*, *ed* uses the first line after *dot* which contains that
string. If the string begins with a minus sign, *ed* searches backward
and uses the last line before *dot* that contains that string (to
search forward for a string that begins with a minus sign, precede the minus
with a backslash).

### API Variables and Functions ###

Data structures:

- *buffers*: dictionary from buffer names (strings) to buffers

- *current*: name of the current buffer

- *buf()*: returns *buffers[current]*, the current buffer

- *buf().lines*: text in the current buffer, a list of lines (strings)

- *buf().o*: Index of current line *dot* in *buf().lines*

- *buf().filename*: filename (string) where the buffer contents are
    written.  Usually the buffer name is the same as the filename, but
    with any directory path prefix removed.

- *buf().unsaved*: True if the current buffer contains unsaved changes

- *lines()*: returns *buf().lines*

- *o*: Same value as *buf().o*, index of *dot* in *lines*

- *S*: Same value as *len(buf().lines) - 1*, index of last line in *lines*

Working with files and buffers:

- *B(name)*: Create a new **B**uffer and load the file *name*.  Print
   the number of lines read (0 when creating a new file). The new
   buffer, also titled *name*, becomes the current buffer.

- *u(name)*: Create a new empty b **u**ffer named *name*.  Do not read
  any file.  The new buffer becomes the current buffer.

- *r(name, i)*: **r**ead file *name* into the current buffer after line
  *i* (default *o*).  Print the number of lines read.

- *b(name)*: Set current **b**uffer to *name*.

- *w(name, i, j)*: **w**rite lines *i* through *j* in current buffer
  (defaults *o* and *S*, the entire buffer) to file *name* (default:
  current buffer name).  Print the file name and the number of lines written.
  Does not change *dot*.

- *D(name)*: **D**elete buffer *name* (default: current buffer).  If 
  buffer has unsaved changes, prompt for confirmation.  

Displaying information:

- *n()*: Print buffer **n**ames.  Current buffer is marked with
  . (period).  Buffers with unsaved changes are marked with *.
  Also print *o*, *S*, and *filename* of each buffer.

- *m()*: Print current line nu **m**ber, *o*.  Also print other status
   information: number of last line *S*, buffer name *current*,
   *filename*.

Displaying and navigating text:

- *p(i, j)*: **p**rint lines *i* through *j* in the current buffer
  (defaults *o,o*).

- *l(i)*: Move *dot* to **l**ine *i* and print it.  Defaults to *o+1*,
  the line after *dot*, so repeatedly invoking *l()* advances through
  the buffer, printing successive lines.  Invoking *l(pattern)* moves
  *dot* to the next line that contains *pattern*, and prints it.

Adding, changing, deleting text:

- *a(i)*: **a**ppend text after line *i* (default *o*), using
   input mode.
   
- . (period at the start of a line in input mode) exit input mode.

- *i(i)*: **i**nsert text before line *i* (default *o*), using
   input mode.

- *c(i,j)*: **c**hange (replace) text from lines *i* through *j*
   (default *o*,*o*), using input mode

- *s(pattern,new,i,j,global)*: **s**ubstitute *new* for *pattern* in lines
   *i* thrugh *j*. When *global* is *True* (the default), substitute
   all occurrences in each line. To substitute only the first
   occurence on each line, set *global* to *False*.  Lines *i,j* default
   to *o,o*.  The special patterns *'%'* and *'$'* indicate the 
   beginning and end of the line.
   
- *d(i,j)*: **d**elete text from lines *i* through *j* (default
   *o*,*o*).  Set *dot* to the first undeleted line.

Command mode:

- *ed()*: Enter command mode.

- *q()*: **q**uit command mode.  No buffers or other context are
  deleted so it is possible to resume the command mode session with
  *ed()* again.


### Command mode ###

For command mode syntax, consult any Unix *ed* reference.  In brief:
one or two line numbers as needed *precede* the single letter command,
separated by commas.  Dot is indicated by a period and the last line
is indicated by the dollar sign *$*.  So the function call to print
the lines around *dot* is:

    p(o-1, o+1)

The corresponding command is:

    .-1,.+1p

The command names are the same as the function names, except *m*
(print line nu **m**ber) is the command *=*, and the function *l*
(move *dot* to line *i* and print) is the empty command - just type a
line number or search string, then *Return*.

### Status ###

These API functions are implemented:

(None)

These commands are implemented:

(None)

Revised Oct 2013
