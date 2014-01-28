
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
can edit directly from the Python prompt.  The following commands have
the same effect as the preceding example.  Notice how all the input
text is the argument to the *a* function, a single multi-line
triple-quoted string.  When running the *piety* Python shell,
you must terminate each line inside the triple quoted string with *^J*
instead of *Return*.

    >>> from ed import *
    >>> B('test.txt')
    0 lines
    >>> a("""ed() enters ed command mode, with the : command  prompt.
    ... 'B <name>' creates a new buffer and loads the named file
    ... 'a' enters ed input mode and appends the text after the current line.
    ... 'w' writes the buffer contents back to the file
    ... 'q' quits ed command mode.
    ... To quit input mode, type a period by itself at the start of a line.""")
    >>> w()
    test.txt, 6 lines

Likewise, you can edit in the buffers with Python commands not
provided in *ed*, for example with any of the string or regular
expression functions or methods.

### Python API conventions ###

Many *ed* functions take arguments indicating a line *i* or a range
of lines *i, j*.  Like Python sequences (but unlike Unix *ed*), line
numbers begin with 0 (not 1), and the range *i,j* includes line *i* but
excludes line *j*.  For example, the range *5,8* includes the three lines
indexed *5,6,7* and the range *5,6* includes just line *5*.

The current line (where, by default, text is changed or inserted) is
called *dot* (indicated in *ed* command mode by a period *.*).  After
most commands, *dot* is updated to the last line affected (the last
line inserted, etc.).  The index of the current line *dot* and the
length of the buffer are returned by the function calls *o()* and
*S()* (which look like the *.* and *$* used in command mode).  The
index of the last line is *S() - 1*, so the range *0,S()* is the whole
buffer.

Line *i* and range *i,j* are always optional.  The default for *i* is
usually *dot* (the current line), the default for *j* (if only *i* is
given) is usually *i+1* (the line after *i*), and the default for *i,j* (if
both are omitted) is usually *.,.+1* (the current line, recall the
second index is not included in the range).  Sometimes the default
range is *0,S()* (the whole buffer).

The functions *f* (or *z*) search forward (or backward) from *dot* for
a given pattern, and return the line number of the first match.  They
implement */pattern/* and *?pattern?* from Unix *ed*.
Typically they are invoked as part of the address expression passed to
a line number argument.

Every Python API function that implements an *ed* command has a signature
like p(*args), with a single-letter name and an argument list declared *args,
so all arguments are optional.  

### Python API summary ###

These are the Python functions and attributes (variables) in
the *ed* module that implement editor commands.  Most functions have
the same single-character names as the commands.  More explanation
follows in the next session.

Data structures:

- *Buffer*: class, defines objects that store text etc.

- *buffers*: dictionary from buffer names (strings) to Buffer instances

- *current*: name of the current buffer where changes are made.

- *buf()*: returns *buffers[current]*, the current buffer

- *buf().lines*: text in the current buffer, a list of lines (strings)

- *buf().dot*: index of current line *dot* in *buf().lines*

- *buf().filename*: filename (string) where the buffer contents are
    written.  Usually the buffer name is the same as the filename, but
    with any directory path prefix removed.

- *buf().unsaved*: True if the current buffer contains unsaved changes

- *buf().pattern*: Search pattern

- *lines()*: returns *buf().lines*

- *o()*: returns *buf().dot*, index of the current line in *lines*.  The
   name *o* resembles the period *.* used to indicae *dot* in *ed*
   command mode.

- *S()*: returns *len(buf().lines)*, the length of the buffer.  The
  index of the last line is *S()-1*.  The name *S* resembles the
  dollar sign *$* used to indicate the end of the buffer in *ed*
  command mode.

Address expressions

- *f(pattern)* - **f**ind, or **f**orward search for *pattern*.
  Return line number of the next occurrence of *pattern* after *dot*.
  Implements */pattern/* and *//* in command mode. 
  If pattern is not found, return *dot*.  Do not update *dot*, but if
  *pattern* is not empty, update the stored pattern.  If *pattern* is
  the empty string, search for the stored pattern.  Typically,
  *f('text')* is invoked as part of the address expression passed to a
  line number argument.

- *z(pattern)* - reverse search for *pattern*.  Like *f*, but searches
  backward from *dot*.    Implements *?pattern?* and *??* in command mode. 

Commands - Working with files and buffers:

- *B(name)*: Create a new **B**uffer and load the file *name*.  Print
   the file name and number of lines read (0 when creating a new
   file). Set *dot* to the last line.  The new buffer, also titled
   *name*, becomes the current buffer.

- *r(name, i)*: **r**ead file *name* into the current buffer after line
  *i* (default .).  Print the file name and number of lines read.
  Set *dot* to the last line read.

- *b(name)*: Set current **b**uffer to *name*.  Do not change its *dot*.
  If no buffer *name*, create a new empty buffer (without reading any file).

- *w(name)*: **w**rite current buffer to file *name* (default: stored
  file name, or if none, current buffer name). Print the file name and
  the number of lines written.  Do not change *dot*.  Change
  *buf().filename* to *name*, so subsequent writes (with no
  argument) go to the same file.

- *D(name)*: **D**elete buffer *name* (default: current buffer).  If
  buffer has unsaved changes, print message and exit without deleting.

- *DD(name)*: **D**elete buffer *name* (default: current buffer).  Like *DD*,
  but deletes without warning even if there are unsaved changes.

Displaying information:

- *e(line)*: **e**valuate address expression to line number and print it.
  Implements *=* in command mode.
  Also print name and other information about the current buffer.  
  Do not chanage *dot*.

- *n()*: Print buffer **n**ames and other information.  Current buffer
  is marked with . (period).  Buffers with unsaved changes are marked
  with an asterisk.  Also print ., *$*, and *filename* of each buffer.

Displaying and navigating text:

- *p(i, j)*: **p**rint lines *i* up to *j* in the current buffer.
    *i* defaults to *dot*, *j* defaults to *i+1*.  
    Change *dot* to the last line printed.

- *l(i)*: Move *dot* to **l**ine *i* and print it.  Defaults to *.+1*,
  the line after *dot*, so repeatedly invoking *l()* advances through
  the buffer, printing successive lines.

Adding, changing, deleting text:

- *a(i, text)*: **a**ppend *text* after line *i* (default .).  Set
   *dot* to the last line appended.
   
- *i(i, text)*: **i**nsert *text* before line *i* (default .).  Set
   *dot* to the last line inserted.

- *c(i,j, text)*: **c**hange (replace) lines *i* up to *j* to *text*.
   (*i,j* default to .,.+1).  Set *dot* to the last replacement line.
   
- *d(i,j)*: **d**elete text from lines *i* up to *j* (default .,.+1).
   Set *dot* to the first undeleted line.

- *s(i,j,pattern,new,global)*: **s**ubstitute *new* for *pattern* in lines
   *i* up to *j*. When *global* is *True* (the default), substitute
   all occurrences in each line. To substitute only the first
   occurence on each line, set *global* to *False*.  Lines *i,j* default
   to .,.+1  Set *dot* to the last changed line.

Shortcuts, conveniences, and composites.  Not yet implemented.

- *k(iline, c)*: mar **k** *iline* with label *c*.  The default line is
*dot*.  When *dot* moves on, the label remains on the marked line
until it is explicitly moved by calling *k* on that label again.  The
default label is *@*, called *mark*.  The lines between *mark*
and *dot*, inclusive, are called the *region*.  If present, the
*region* is the default text range for several commands.  If no line
is labelled with *mark*, the region is the line at *dot*.  In Unix *ed*, 
the label *c* must be a single lower-case character, but in *ed.py* it
can be any string.  The label *@* has no special meaning in Unix *ed*.

- *F(c)*: return the line number at label *c*, or None of there is no such line.
  Implements *'c* in *ed*.

- *K(label)*: unmar **K**, remove *label* from its line, wherever it may be.
  Again, the default label is the mark, *@*.

- *m(i,j,k,buffer)*: **m**ove selected lines, insert at given line in
   selected *buffer*.

- *t(i,j,k,buffer)*: **t**ransfer (copy) selected lines, insert at given line 
   in selected *buffer*.

- *x(i,j)*: *cut*, move selected lines into *paste* buffer,
  overwriting previous paste buffer contents.

- *X(i,j)*: *copy* selected lines into *paste* buffer.

- *y(k,buffer)*: **y**ank, insert contents of paste buffer given line in
   given buffer, default *dot*.

Command mode:

- *ed()*: Enter command mode.

- *q()*: **q**uit command mode.  No buffers or other context are
  deleted so it is possible to continue editing using the Python API,
  or to resume the command mode session with *ed()* again.

### Command mode ###

For command mode syntax, consult any Unix *ed* reference.  In brief:
one or two line numbers as needed *precede* the single letter command,
separated by commas.  Dot is indicated by a period and the length of
the buffer is indicated by the dollar sign *$*.  So the function call
to print the from the line before *dot* to three lines before the end
is:

    p(o()-1,S()-3)

The corresponding command is:

    .-1,$-3p

The command names are the same as the function names, except *e*
(**e**valuate line number) is the command *=*, and the function *l*
(move *dot* to line *i* and print) is the empty command - just type a
line number or search string, then *Return*.  Just pressing *Return* 
advances *dot* to the next line and prints it.

### Status ###

These API variables and functions are implemented:

*buffers, current, buf, lines, o, S, f, z, r, b, B, w, D, DD, n, e, p,
 l, a, i, d, c, s*

Also *ed* and *q* to enter and quit *ed* command mode.

Limitations:

In the **s**ubstitute function, the *pattern* must be literal string, not a 
regular expression.  

In the *f* and *z* functions, the search *pattern* must be a literal
string, not a regular expression.  The program searches only to end
(or beginning) of the buffer, with no wraparound.

The *ed* command mode is barely working.  All commands are
implemented, but only as (single character) command names with no
arguments.  Commands that have default argument values use them, but
many commands are not yet useful.  Command mode blocks when waiting
for a command, so it does not yet work with the Piety scheduler.

Revised Jan 2014
