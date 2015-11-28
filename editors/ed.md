
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
  [edsel](edsel.md).

## Commands ##

**ed.py** supports these commands from classic *ed*:

 *= ! a c d e E f i k l m p q r s t w z*

**ed.py** supports these line address forms from classic *ed*:

 *number . , ; % $ 'c /text/ // ?text? ?? +number -number ^number* also *+ ++*  etc. *- --* etc. *^ ^^* etc.

**ed.py** also supports these commands from *sam*:

 *b B D n*

**ed.py** also adds a *y* (yank) command that inserts the lines most
recently deleted by the *d* command (possibly from a different
buffer).  A *d* command followed by one or two *y* commands can achieve the
effect of the classic *ed* *m* (move) or *t* (transfer, or copy)
commands, and can also move lines to another buffer.

Here is a [command summary](ed.txt).

Classic *ed* is described in many books: *The Unix Programming
Environment* by Kernighan and Pike, *Software Tools* by Kernighan and
Plauger, etc.  Or just type *man ed* on any Unix-like system
(including Mac OS X).  The version of *ed* in Plan 9 is almost the
same, and is described in a completely rewritten man page at
[http://plan9.bell-labs.com/magic/man2html/1/ed](http://plan9.bell-labs.com/magic/man2html/1/ed)
and
[http://man.cat-v.org/plan_9/1/ed](http://man.cat-v.org/plan_9/1/ed).
There is a brief tutorial at a recent [blog](http://blog.sanctum.geek.nz/actually-using-ed/), with more comments and links
at [HN](https://news.ycombinator.com/item?id=4120513).

The *sam* editor is described at
[http://plan9.bell-labs.com/sys/doc/sam/sam.html](http://plan9.bell-labs.com/sys/doc/sam/sam.html)
and [http://sam.cat-v.org/](http://sam.cat-v.org/).

**ed.py** can run as a standalone program: *python ed.py* (it takes no
command line options or arguments).  But *ed* is intended to run in an
interactive Python session.  Here is a brief example:

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

The *ed.main()* function takes one optional positional argument, the
file name, and one optional keyword argument, *p* the command prompt
string.  Type *ed.main('test.txt')* to begin editing *test.txt*, as if
you had typed *ed.main()* and then *e test.txt*.  Type
*ed.main(p=':')* to use a single colon as the command prompt (the
default prompt is the empty string).  The file name and prompt can
appear together, so you can type *ed.main('test.txt', p=':')*.

In *!command*, the *command* is passed to the Python interpreter, not
to the system command shell as in classic *ed*.  Use this to execute
Python statements without leaving *ed* command mode.  For example, you
can use this to change the command prompt at any time during an editing session:
*!ed.prompt = ':'*

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
**ed.py** imports *buffer.py*, which provides the *Buffer* class,
which defines the core data structure and the internal API for
updating it.  Many *Buffer* methods correspond to functions in the
API, but here each method has a fixed argument list, provides no error
checking, and no error messages or progress messages.  The *Buffer*
class does not access the console, but updates text buffers and reads
and writes files.

The *Buffer* class provides a *write* method so other code can update
text buffers without using the *ed.py* user interface or API, by
calling the standard Python *print* function.  The *Buffer* class has
an *update* attribute which can optionally be assigned to a callable
that may be used by the *write* method to update a display (for
example).


## Limitations ##

**ed.py** does not support these classic *ed* commands: 
*H h j n P Q u wq W x*.  Some of these might be supported in the
future.

**ed.py** supports the *sam* command *n* (print list of buffers),
not the classic *ed* command *n* (print line numbers).

**ed.py** does not support the classic *ed* *p* command suffix (for
printing the current line after any command).

**ed.py** does not support the classic *ed* iteration commands *g G v V*.

**ed.py** does not warn about the quit command *q* when there are
unsaved buffers, because the session with all its buffers can be
resumed by calling *ed.main()* at the Python interpreter prompt again.

**ed.py** always prints the error message following the *?* character.
There is no way to suppress printing the error messages as in classic
*ed*.

In the *s* (substitute) command and in the */text/* and *?text?*
address forms, the text pattern is ordinary text, not a regular
expression.  Regular expressions might be supported in the future.

In the */text/* and *?text?* address forms, **ed.py** only searches
forward to the end of the buffer (or backward to the beginning). It
does not wrap around and continue searching from the beginning (or
end).

The *B* (and *D*) commands accept only one file (or buffer) name argument, 
not multiple names as in *sam*.


Revised November 2015
