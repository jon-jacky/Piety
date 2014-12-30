
ed.py
==

**ed.py** is a text editor in pure Python inspired by the classic Unix
editor *ed*.  It provides many of the commands from *ed*, augmented
with a few commands for handling multiple buffers and files from the
later Unix (and Plan 9) editor *sam*.  You can use **ed.py** in a
command mode that emulates classic *ed*, or use its API to edit from
the Python prompt or write editing scripts in Python.

**ed.py** can wait for input without blocking, so it can run with a
cooperative multitasking system such as [Piety](../piety/README.md).

**ed.py** provides the command line and internals for the display editor
  [edd](edd.md).

## Commands ##

**ed.py** supports these commands from classic *ed*:

 *= ! a c d e E f i l p q r s w z*

**ed.py** supports these line address forms from classic *ed*:

 *number . , ; % $ /text/ // ?text? ?? +number -number ^number* (but not bare *+ - ^*)


**ed.py** also supports these commands from *sam*:

 *b B D n*

Here is a [command summary](ed.txt).

Classic *ed* is described in many books: *The Unix Programming
Environment* by Kernighan and Pike, *Software Tools* by Kernighan and
Plauger, etc.  Or just type *man ed* on any Unix-like system
(including Mac OS X).  The version of *ed* in Plan 9 is almost the
same, and is described in a completely rewritten man page at
[http://plan9.bell-labs.com/magic/man2html/1/ed](http://plan9.bell-labs.com/magic/man2html/1/ed)
and
[http://man.cat-v.org/plan_9/1/ed](http://man.cat-v.org/plan_9/1/ed).

The *sam* editor is described at
[http://plan9.bell-labs.com/sys/doc/sam/sam.html](http://plan9.bell-labs.com/sys/doc/sam/sam.html)
and [http://sam.cat-v.org/](http://sam.cat-v.org/).

**ed.py** can run as a standalone program: *python ed.py*.  But *ed* is
intended to run in an interactive Python session.  Here is a brief
example:

    >>> import ed
    >>> ed.main()
    e test.txt
    test.txt, 0 lines
    a
    ed.main() enters ed command mode.  By default, there is no command prompt.
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
*ed.main()* again.

In *!command*, the *command* is passed to the Python interpreter, not 
to the system command shell as in classic *ed*.  Use this
to execute Python statements without leaving *ed* command mode.

## API ##

**ed.py** has a Python API so you can edit from the Python prompt or
write editing scripts in Python.  Here is the preceding example
expressed using the API.  Here we use the *from ed import ...* form
so we don't have to prefix each function call with *ed.*

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

The API also provides a function *cmd* with a single string
argument, which is exactly the command string you would type to *ed*
in command mode or the text string you would type in input mode.  Here
is the preceding example expressed once more using *ed.cmd*:

    >>> import ed
    >>> ed.cmd('e test.txt')
    test.txt, 0 lines
    >>> ed.cmd('a')
    >>> ed.cmd('ed() enters ed command mode.  By default, there is no command prompt.')
    >>> ed.cmd("'e <name>' loads the named file into the current buffer.")
    >>> ed.cmd("'a' enters ed input mode and appends the text after the current line.")
    >>> ed.cmd("'w' writes the buffer contents back to the file")
    >>> ed.cmd("'q' quits ed command mode.")
    >>> ed.cmd('To quit input mode, type a period by itself at the start of a line.')
    >>> ed.cmd('.')
    >>> ed.cmd('w')
    test.txt, 6 lines

When **ed.py** is running with the *Piety* cooperative multitasking
scheduler, *Piety* collects a command line or input line without
blocking, and then passes that line to *ed.cmd*.

## Modules ##

**ed.py** provides the user interface: the command line and the public
Python API described above, including command line parsing, argument
checking, and error messages.  **ed.py** reads and writes at the
console, but does not directly update buffers or access files.
**ed.py** imports *ed0.py*, which provides the core: the data
structures and the internal API for updating them, where each function
has a fixed argument list, provides no error checking, and no error
messages or progress messages.  *ed0.py* does not access the
console, but updates buffers and reads and writes files.

## Limitations ##

**ed.py** does not support these classic *ed* commands: 
*H h j k m n P Q t u wq W*.  Some of these might be supported in the
future.

**ed.py** supports the *sam* command *n* (print list of buffers),
not the classic *ed* command *n* (print line numbers).

**ed.py** does not support these classic *ed* address forms: *+ - ^ 'c*.
Some of these might be supported in the future
(*+number -number ^number* are already supported).

**ed.py** does not support the classic *ed* *p* command suffix (for
printing the current line after any command).

**ed.py** does not support the classic *ed* iteration commands *g G v V*.

In the *s* (substitute) command and in the */text/* and *?text?*
address forms, the text pattern is ordinary text, not a regular
expression.  Regular expressions might be supported in the future.

In the */text/* and *?text?* address forms, **ed.py** only searches
forward to the end of the buffer (or backward to the beginning). It
does not wrap around and continue searching from the beginning (or
end).

The *B* (and *D*) commands accept only one file (or buffer) name argument, 
not multiple names as in *sam*.

There is no way to move text from one buffer to another.  This might
be fixed in the future by defining extensions to the move and copy
commands, *m* and *t*.

Revised October 2014
