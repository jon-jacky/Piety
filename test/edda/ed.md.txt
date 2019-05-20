
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

Lines *i* and *j* can be identified by the patterns (substrings) they
contain, instead of their integer indices.  If you provide a string
*/text/* instead of a number for the *i* or *j* argument, *ed* uses
the first line after *dot* which contains *text*.  To search backward
from *dot*, use *\text\*. (This feature is not yet implemented.)

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

- *lines()*: returns *buf().lines*

- *o()*: returns *buf().dot*, index of the current line in *lines*.  The
   name *o* resembles the period *.* used to indicae *dot* in *ed*
   command mode.

- *S()*: returns *len(buf().lines)*, the length of the buffer.  The
  index of the last line is *S()-1*.  The name *S* resembles the
  dollar sign *$* used to indicate the end of the buffer in *ed*
  command mode.

Commands - Working with files and buffers:

- *B(name)*: Create a new **B**uffer and load the file *name*.  Print
   the file name and number of lines read (0 when creating a new
   file). Set *dot* to the last line.  The new buffer, also titled
   *name*, becomes the current buffer.

- *u(name)*: Create a new empty b **u**ffer named *name*.  Do not read
  any file.  The new buffer becomes the current buffer.

- *r(name, i)*: **r**ead file *name* into the current buffer after line
  *i* (default .).  Print the file name and number of lines read.
  Set *dot* to the last line read.

- *b(name)*: Set current **b**uffer to *name*.  Do not change its *dot*.

- *w(name)*: **w**rite current buffer to file *name* (default: stored
  file name, or if none, current buffer name). Print the file name and
  the number of lines written.  Do not change *dot*.  Change
  *buf().filename* to *name*, so subsequent writes (with no
  argument) go to the same file.

- *D(name)*: **D**elete buffer *name* (default: current buffer).  If
  buffer has unsaved changes, prompt for confirmation (the
  confirmation prompt is not currently implemented).

Displaying information:

- *n()*: Print buffer **n**ames.  Current buffer is marked with
  . (period).  Buffers with unsaved changes are marked with an asterisk.
  Also print ., *$*, and *filename* of each buffer.

- *m()*: Print current line nu **m**ber, *dot*.  Also print number of
   lines *$*, buffer name *current*, and its *filename*.

Displaying and navigating text:

- *p(i, j)*: **p**rint lines *i* up to *j* in the current buffer.
    *i* defaults to *dot*, *j* defaults to *i+1*.  
    Change *dot* to the last line printed.

- *l(i)*: Move *dot* to **l**ine *i* and print it.  Defaults to *.+1*,
  the line after *dot*, so repeatedly invoking *l()* advances through
  the buffer, printing successive lines.  Invoking *l(/text/)* moves
  *dot* forward to the next line that contains *text*, and prints it.
  *l(\text\\)* moves *dot* backward.

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

The command names are the same as the function names, except *m*
(print line nu **m**ber) is the command *=*, and the function *l*
(move *dot* to line *i* and print) is the empty command - just type a
line number or search string, then *Return*.  Just pressing *Return* 
advances *dot* to the next line and prints it.

### Status ###

These API variables and functions are implemented:

*buffers, current, buf, lines, o, S, B, b, w, D, n, m, p, l, a, i, d, u, r, c, s*

These commands are implemented:

(None)

For now, line addresses *i* and *j* must be integers.  Text patterns are not
yet supported.

Revised Dec 2013
