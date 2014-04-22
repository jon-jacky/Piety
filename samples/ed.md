
ed
==

**ed** is a line-oriented text editor written in pure Python.  It
provides many of the commands from the classic Unix editor *ed*,
augmented with a few commands for handling multiple buffers and files
from the later Unix (and Plan 9) editor *sam*.  You can use **ed** in
a command mode that emulates classic *ed*, or use its API to edit from
the Python prompt or write editing scripts in Python.

## Commands ##

**ed** supports these commands from classic *ed*:

 *= a c d e E f i l p q r s w*

**ed** supports these line address forms from classic *ed*:

 *number . , ; % $ /text/ ?text?*

Classic *ed* is described in many books: *The Unix Programming
Environment* by Kernighan and Pike, *Software Tools* by Kernighan and
Plauger, etc.  Or just type *man ed* on any Unix-like system
(including Mac OS X).  The version of *ed* in Plan 9 is almost the
same, and is described in a completely rewritten man page at
[http://plan9.bell-labs.com/magic/man2html/1/ed](http://plan9.bell-labs.com/magic/man2html/1/ed)
and
[http://man.cat-v.org/plan_9/1/ed](http://man.cat-v.org/plan_9/1/ed).

**ed** also supports these commands from *sam*:

 *b B D n*

The *sam* editor is described at
[http://plan9.bell-labs.com/sys/doc/sam/sam.html](http://plan9.bell-labs.com/sys/doc/sam/sam.html)
and [http://sam.cat-v.org/](http://sam.cat-v.org/).

**ed** can run as a standalone program, but is intended to run in an
interactive Python session.  Here is a brief example:

    >>> from ed import *
    >>> ed()
    e test.txt
    test.txt, 0 lines
    a
    ed() enters ed command mode.  By default, there is no command  prompt.
    'e <name>' loads the named file into the current buffer.
    'a' enters ed input mode and appends the text after the current line.
    'w' writes the buffer contents back to the file.
    'q' quits ed command mode.
    To quit input mode, type a period by itself at the start of a line.
    .
    w
    test.txt, 6 lines
    q
    >>>

After the *q* command, all the editor buffers and other context
remain, so the editing session can be resumed at any time by typing
*ed()* again.

## API ##

**ed** has a Python API so you can edit from the Python prompt or
write editing scripts in Python.  Here is the preceding example
expressed using the API:

    >>> from ed import *
    >>> e('test.txt')
    test.txt, 0 lines
    >>> a("""ed() enters ed command mode.  By default, there is no command prompt.
    ... 'e <name>' loads the named file into the current buffer.
    ... 'a' enters ed input mode and appends the text after the current line.
    ... 'w' writes the buffer contents back to the file
    ... 'q' quits ed command mode.
    ... To quit input mode, type a period by itself at the start of a line.""")
    >>> w()
    test.txt, 6 lines

All of the text for the append command *a* is handled here as the
argument to the *a* function, expressed as a single multi-line
triple-quoted string.  (The dots ... preceding each continuation line
are printed by the interactive Python interpreter, they are not part
of the string argument.)

For every supported *ed* command there is a corresponding API function
with the same name (the *A* (for address) function implements *=*).
Usually all of the arguments are optional (the functions are all
defined with *args argument lists).

Arguments appear in the same order as they do in command mode, so the
*ed* print commands *p* *1p* and *1,4p* correspond to the API print
function calls *p()* *p(1)* and *p(1,4)*.  Likewise, the
substitute command *14s/old/new/g* correponds to the function call
*s(14,'old','new',True)*. 

The line address forms *. $ /text/ ?text?* correspond to the function
calls *o() S() F(text) R(text)*.  For example, the print commands *.,$p* and
*/text/p* correspond to function calls *p(o(),S())* and *p(F('text'))*.


## Modules ##

**ed** comprises two modules.  *ed.py* provides both the commands and
the public Python API.  *ed0.py* provides the core: the data
structures and the internal API for updating them, where each function has
a fixed argument list, provides no error checking, and no error
messages or progress messages.

## Limitations ##

**ed** does not support these classic *ed* commands: 
*H h j k m n P Q t u wq W z*.  Some of these might be supported in the
future.

**ed** does not support the classic *ed* address forms *+ - ^ -n ^n +n*.
Some of these might be supported in the future.

**ed** does not support the classic *ed* *p* command suffix (for
printing the current line after any command).

**ed** does not support the classic *ed* iteration commands *g G v V*.

In the *s* (substitute) command and in the */text/* and *?text?*
address forms, the text pattern is ordinary text, not a regular
expression.  Regular expressions might be supported in the future.

In the */text/* and *?text?* address forms, **ed** only searches
forward to the end of the buffer (or backward to the beginning). It
does not wrap around and continue searching from the beginning (or
end).

The *B* command accepts only one file name argument, not multiple file
names as in *sam*.

There is no way to move text from one buffer to another.  This might
be fixed in the future by defining extensions to the move and copy
commands, *m* and *t*.

In command mode, **ed** blocks while waiting for the next command, so
it cannnot work with a cooperative mulitasking scheduler such as
*piety*.  We plan to fix this.

Revised Apr 2014
