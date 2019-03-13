
ed.py
=====

**[ed.py](ed.py)** is a text editor in pure Python inspired by the
classic Unix editor *ed*.  It provides most of the commands from
classic *ed* and *GNU ed*, augmented with a few commands for handling
multiple buffers and files from the later Unix (and Plan 9) editor
*sam*.  You can use **ed.py** in a command mode that emulates classic
*ed*, or use its API to edit from the Python prompt or write editing
scripts in Python.

**ed.py** runs its editor functions quickly without blocking,
so it can run with a cooperative multitasking system such as
[Piety](../piety/README.md).

**ed.py** provides the command line and internals for the display editors
  [edsel](edsel.md) and [eden](eden.md).

**ed.py** has no dependencies.

## Running ed.py ##

**ed.py** can run as a standalone program or in an interactive Python session.

The recommended way to run **ed.py** as a standalone program is:

    python3 -i -m ed

Here the *-i* option runs Python in interactive mode so you can use
*readline*-style editing in commands and input text.  The *-i* option
also makes it possible to resume an *ed.py* session
after exiting or after a program crash (see below).

The *-m* option finds
and runs **ed.py** from any directory on your Python path (here you provide
the module name *ed*, not the file name *ed.py*).

**ed.py** provides a few command line arguments and options, explained in this
output from *ed -h*:

    usage: ed.py [-h] [-p PROMPT] [file]

    positional arguments:
      file                  name of file to load into main buffer at startup (omit
                            to start with empty main buffer)

    optional arguments:
      -h, --help            show this help message and exit
      -p PROMPT, --prompt PROMPT
                            command prompt string (default ':')

For example, to load the file *lines20.txt* on startup and use the
precent sign *%* as the prompt string:

    python3 -i -m ed lines20.txt -p %
    lines20.txt, 20 lines
    %

The default prompt string is the colon *:*.  To run with no prompt string,
like classic *ed*, use *-p ''*.

To run *ed.py* in an interactive Python session, type *from ed import* *
to import the entire API.   Then type *ed()* to start the editor:

    python3 -i
    ...
    >>> from ed import *
    >>> ed()
    :

The *ed* function accepts an optional positional argument for a file name and
and optional keyword argument for a prompt string, so the *ed* function call
can resemble the *ed* command line:

    >>> ed('lines20.txt', p='%')
    lines20.txt, 20 lines
    %

## Stopping and resuming ed.py ##

The usual way to stop *ed.py* is to use its *q* (quit) command.
You can also interrupt *ed.py* by typing *^C*.  It is possible
that *ed.py* might crash due to a programming error or other
unhandled exception.

If you start *ed.py* with a Python command that includes
the *-i* option, control transfers to an
interactive Python prompt when *ed.py* stops for any reason.
All the editing buffers and their contents are still intact.
You can use the *ed.py* API or any other Python statements.
You can type *ed()* to resume running *ed.py* again.
You can exit the Python session in the usual
way, by typing *exit()* or *^D*.

## Commands ##

**ed.py** supports these commands from classic *ed*:

 *= a c d e E f i j k l m p q Q r s t w z*

**ed.py** supports these commands from *GNU ed*:

 *# x y*

**ed.py** supports these commands from *sam*:

 *b B D n*

In the *b* command, the buffer name parameter can be abbreviated by
providing a prefix followed by a hyphen -- a sort of "poor person's
tab completion".  For example, the command *b key-* or even *b k-*
might switch to the buffer *keyboard.py*.  If more than one buffer
name begins with the same prefix, *ed.py* just chooses one.

**ed.py** supports these line address forms from classic *ed*:

 *number . , ; % $ 'c /text/ // ?text? ?? +number -number ^number* also *+ ++*  etc. *- --* etc. *^ ^^* etc.

Here is a [command summary](ed.txt).

Classic *ed* is described in many books: *The Unix Programming
Environment* by Kernighan and Pike, *Software Tools* by Kernighan and
Plauger, etc.  Or just type *man ed* on any Unix-like system
(including Mac OS X).  The version of *ed* in Plan 9 is almost the
same, and is described in a completely rewritten man page at
[http://plan9.bell-labs.com/magic/man2html/1/ed](http://plan9.bell-labs.com/magic/man2html/1/ed)
and
[http://man.cat-v.org/plan_9/1/ed](http://man.cat-v.org/plan_9/1/ed).
There is a manual at [GNU](http://www.gnu.org/software/ed/manual/ed_manual.html),
and a brief tutorial at a [blog](http://blog.sanctum.geek.nz/actually-using-ed/),
with more comments and links
at [HN](https://news.ycombinator.com/item?id=4120513).  There is even a [POSIX standard](http://pubs.opengroup.org/onlinepubs/9699919799/utilities/ed.html).

The *sam* editor is described at
[http://plan9.bell-labs.com/sys/doc/sam/sam.html](http://plan9.bell-labs.com/sys/doc/sam/sam.html)
and [http://sam.cat-v.org/](http://sam.cat-v.org/).

This brief example that shows how to invoke **ed.py** in an
interactive Python session and run some commands:

    >>> from ed import *
    >>> ed()
    :e test.txt
    test.txt, 0 lines
    :a
    ed.main() enters ed command mode.  By default, there is no command prompt.
    'e <name>' loads the named file into the current buffer.
    'a' enters ed input mode and appends the text after the current line.
    'w' writes the buffer contents back to the file.
    'q' quits ed command mode.
    To quit input mode, type a period by itself at the start of a line.
    .
    :w
    test.txt, 6 lines
    :q
    >>>

After the *q* command, all the editor buffers and other context
remain, so the editing session can be resumed at any time by calling
*ed()* again.  Or, any of the other API functions can be called
at the Python prompt.

The *n* command prints information about all the buffers,
for example:

    CRM Buffer            Lines  Mode     File
        ed.py                 1  Text     ed.py
      * notes.txt        104528  Text     /users/jon/notes/piety/notes/notes.txt
        main                  1  Text     None
    .   ed.md               300  Text     ed.md

The dot in the *C* (current) column indicates the current buffer.
A percent sign *%* in the *R* (readonly) column indicates that
buffer is read-only.  An asterisk *** in the M (modified) column
indicates the buffer contains unsaved changes.

## Limitations and differences from classic ed and sam ##

**ed.py** does not support these classic *ed* commands:
*H h n P u wq W*.  Some of these might be supported in the
future.

**ed.py** does not support the classic *ed* iteration commands *g G v V*.

**ed.py** does not support the classic *ed* *p* command suffix (for
printing the current line after any command).

**ed.py** supports the *sam* command *n* (print list of buffers),
not the classic *ed* command *n* (print line numbers).

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

The default prompt is the colon *:*, not the empty string.  If no
prompt is desired, that must be requested with *-p ''* on the command
line or *p=''* in the *ed* function call.

The *z* command accepts a negative parameter to scroll backward,
unlike classic *ed*.

## API ##

**ed.py** has a Python API so you can edit from the Python prompt or
write editing scripts in Python.  Here is the preceding example
expressed using the API.  Here we use the *from ed import* * form
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

For every supported *ed* command there is a corresponding API *command
function* with the same single-letter name (the *A* (for address) function
implements *=*).  Usually all of the arguments are optional (the
functions are all defined with *args argument lists).    Each API command
function gathers and checks its own arguments, providing defaults as needed.

Arguments appear in the same order as they do in command mode, so the
*ed* print commands *p* *1p* and *1,4p* correspond to the API print
function calls *p()* *p(1)* and *p(1,4)*.  Likewise, the
substitute command *14s/old/new/g* correponds to the function call
*s(14,'old','new',True)*.

The line address forms *. $ /text/ ?text?* correspond to the function
calls *o() S() F(text) R(text)*.  For example, the print commands *.,$p* and
*/text/p* correspond to function calls *p(o(),S())* and *p(F('text'))*.

The API also provides a function *do_command* with a single string
argument, which is exactly the command string you would type to *ed*
in command mode or the text string you would type in input mode.  Here
is the preceding example expressed once more using *do_command*:

    >>> from ed import *
    >>> do_command('e test.txt')
    test.txt, 0 lines
    >>> do_command('a')
    >>> do_command('ed() enters ed command mode.  By default, there is no command prompt.')
    >>> do_command("'e <name>' loads the named file into the current buffer.")
    >>> do_command("'a' enters ed input mode and appends the text after the current line.")
    >>> do_command("'w' writes the buffer contents back to the file")
    >>> do_command("'q' quits ed command mode.")
    >>> do_command('To quit input mode, type a period by itself at the start of a line.')
    >>> do_command('.')
    >>> do_command('w')
    test.txt, 6 lines

When **ed.py** is running with the *Piety* cooperative multitasking
scheduler, *Piety* collects a command line or input line without
blocking, and then passes that line to *do_command*.

## Modules ##

**[ed.py](ed.py)** provides the user interface: the command line and the public
Python API described above, including command line parsing, argument
checking, and error messages.  **ed.py** reads and writes at the
console, but does not directly update buffers or access files.

**ed.py** imports the *buffer.py* module, which provides the
*Buffer* class, which defines the core data structure and the internal
API for updating it.  Many *Buffer* methods correspond to functions in
the API, but here each method has a fixed argument list, provides no
error checking, and no error messages or progress messages.  The
*Buffer* class does not access the console, but updates text buffers
and reads and writes files.

**ed.py** imports the *parse.py* module that provides
functions for parsing the *ed* command line, and the
*check.py* module that provides functions for checking
command arguments and supplying default arguments.

**ed.py** imports the *view.py* module, which contains configuration
variables that are read and written by both *ed* and the display
editor *edsel*, in order to configure code used by both programs to
run with or without a display.

**ed.py** imports the *Op* display operations enumeration from the
*updates.py* module, which appears in code in *ed* that is also used
by the *edsel* display editor.

The *buffer*, *parse*, *check*, *view*, and *updates* modules are
included in this directory.  **ed.py** also uses the Python standard
library modules *re*, *os*, and *sys*.  Other than that, **ed.py** has
no dependencies.

Revised Mar 2019

