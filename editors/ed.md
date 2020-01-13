
ed.py
=====

**[ed.py](ed.py)** is a text editor in pure Python inspired by the
classic Unix editor *ed*.

**ed.py** provides most of the commands from
classic *ed* and *GNU ed*, augmented with a few commands for handling
multiple buffers and files from the later Unix (and Plan 9) editor
*sam*.

**ed.py** runs in a command mode that emulates classic
*ed*.  It also provides an API so you can edit from the Python prompt
or write editing scripts in Python.

**ed.py** has no dependencies.

## Running ed.py ##

**ed.py** can run as a standalone program or in an interactive Python session.

The recommended way to run **ed.py** as a standalone program is:

    python3 -i -m ed

Here *python3* runs Python version 3 on my system (where the default
*python* command still runs Python version 2).
The *-i* option runs Python in interactive mode so you can use
*readline*-style editing in commands and input text.  The *-i* option
also makes it possible to resume an *ed.py* session
after exiting, or to recover from a program crash, without losing buffer
contents in memory that have not yet been saved to a file.

The *-m* option finds
and runs **ed.py** from any directory on your Python path (here you provide
the module name *ed*, not the file name *ed.py*).

Both options can be put together: *-im*

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

    python3 -im ed lines20.txt -p %
    lines20.txt, 20 lines
    %

The default prompt string is the colon *:*.  To run with no prompt string,
like classic *ed*, you must specify the empty string: *-p ''*.

To run *ed.py* in an interactive Python session, type *import ed*
to import the entire API, including the *main* function.
Then type *ed.main()* to start the editor:

    ...$ python3 -i
    ...
    >>> import ed
    >>> ed.main()
    :

The *main* function accepts an optional positional argument for a file name and
and optional keyword argument for a prompt string, so the *main* function call
can resemble the *ed* command line:

    >>> ed.main('lines20.txt', p='%')
    lines20.txt, 20 lines
    %

## Stopping and resuming ed.py ##

The usual way to stop *ed.py* is to use its *q* (quit) command
(the *Q* command quits without warning about any unsaved changes).
You can also interrupt *ed.py* by typing *^C*.  It is possible
that *ed.py* might crash due to a programming error or other
unhandled exception.

If you start *ed.py* with a Python command that includes the *-i* option,
control transfers to an
interactive Python prompt when *ed.py* stops for any reason.
All the editing buffers, their contents, and other
context -- such as the current line in each buffer -- are still intact.
You can use the *ed.py* API or any other Python statements.

To restart *ed.py* from the Python prompt, resuming just where
you left off, type *main()* (or *ed.main()* if you started with *import ed*).
No function arguments
are needed this time, because the arguments used at startup are still in effect.

You can exit the Python session in the usual
way, by typing *exit()* or *^D*.   Then the buffer contents are
lost and it is no longer possible to resume the session.

## Commands ##

**ed.py** supports these commands from classic *ed*:

 *= a c d e E f i j k l m p q Q r s t w z*

**ed.py** supports these commands from *GNU ed*:

 *# x y*

**ed.py** supports these commands from *sam*:

 *b B D n*

**ed.py** add new *wrap*, *indent*, *buffers*, and *outdent* commands:

 *J I N O*

**ed.py** supports these line address forms from classic *ed*:

 *number . , ; % $ 'c /text/ // ?text? ?? +number -number ^number* also *+ ++*  etc. *- --* etc. *^ ^^* etc.

**ed.py** adds a new line address form *[* to indicate the region from  
the *mark* to *dot*.

Here is a [command summary](ed.txt).

Classic *ed* is described in many books: *The Unix Programming
Environment* by Kernighan and Pike, *Software Tools* by Kernighan and
Plauger, etc.  Or just type *man ed* on any Unix-like system
(including Mac OS X).  The version of *ed* in Plan 9 is almost the
same, and is described in a completely rewritten man page at
[http://man.cat-v.org/plan_9/1/ed](http://man.cat-v.org/plan_9/1/ed).
There is a manual at [GNU](http://www.gnu.org/software/ed/manual/ed_manual.html),
and a brief tutorial at a [blog](http://blog.sanctum.geek.nz/actually-using-ed/),
with more comments and links
at [HN](https://news.ycombinator.com/item?id=4120513).  There is even a [POSIX standard](http://pubs.opengroup.org/onlinepubs/9699919799/utilities/ed.html).

The *sam* editor is described at [http://sam.cat-v.org/](http://sam.cat-v.org/).

This brief example that shows how to invoke **ed.py** in an
interactive Python session and run some commands:

    >>> import ed
    >>> ed.main()
    :e test.txt
    test.txt, 0 lines
    :a
    ed.main() enters ed command mode.  By default, the command prompt is :
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

After the *q* or *Q* command, all the editor buffers and other context
remain, so the editing session can be resumed at any time by calling
*main()* again.  Or, any of the other API functions can be called
at the Python prompt.

### Working with files and buffers ###

**ed.py** can work on several (or many) files in the same session.
The contents of each file are stored in a separate named *buffer*.
There is always one *current buffer* where editing commands take effect.
When *ed.py* starts up, there is one buffer named *main*.

The *n* command prints information about all the buffers,
for example:

    CRM Buffer            Lines  Mode     File
        ed.py               514  Text     ed.py
      * notes.txt        104528  Text     /users/jon/notes/piety/notes/notes.txt
        main                  1  Text     (no file)
    .   ed.md               335  Text     ed.md

The *N* command writes the same information into a buffer name *Buffers*.

The dot in the *C* (current) column indicates the current buffer.
A percent sign *%* in the *R* (readonly) column indicates that
buffer is read-only.  An asterisk * in the *M* (modified) column
indicates the buffer contains unsaved changes.  The buffer size
is given in lines (not characters). At this time
the only mode we provide is *Text* and there are no read-only buffers.

A buffer can have a file name, the file where buffer contents
are written by a *w* (write) command with no parameter.
The *w* or *f* (file name) commands with a file name
parameter assign or reassign the buffer's file name.

It is possible to create a *scratch buffer* that has
no file name, so a *w* command with no parameter
writes out nothing (it just prints an error message).
Scratch buffer contents can be written out by a *w* command
with a file name parameter, or after assigning a file name with
the *f* command.

The *B* command creates a new buffer and reads a file into it.
The name of the file is the *B* command parameter, which might
be in the current default directory, or might include a prefix
that names a directory path.  This becomes the new buffer's file name.
If the file does not already exist, *ed.py* creates it when
it writes out the buffer.  The name of the new buffer itself
is the file's basename (without any path prefix).

If one or more  buffers contain files with the same basename (for
example, several *README.md* from different directories),
the *B* command makes the buffer names unique by adding suffixes:
*README.md<1>*, *README.md<2>* etc.

The *b* command takes a buffer name parameter and makes that
the current buffer.

In the *b* command, if the buffer name parameter is omitted,
the previous buffer is made current.  This makes it easy to switch
between buffers.

In the *b* command, the buffer name parameter can be abbreviated by
providing a prefix followed by a hyphen -- a sort of "poor person's
auto completion".  For example, the command *b key-* or even *b k-*
might switch to the buffer *keyboard.py*.  If more than one buffer
name begins with the same prefix, *ed.py* just chooses one.

In the *b* command, if the buffer name parameter is given but
there is no buffer with that name, an empty scratch buffer
with that name is created.

The *e* and *E* commands load a different file into an
existing buffer, overwriting the previous contents
and re-assigning the file name (the E command skips
the 'unsaved changes' warning).
They are provided for compatibility with classic *ed*,
but in *ed.py* they only work in the *main* buffer.

To help prevent losing work by accidentally writing over
a file with the wrong buffer contents,
*ed.py* ensures that a file can be stored in
only one buffer at a time.  If the *B* command is given with
the name of a file that is already stored in a buffer, no new
buffer is created, instead the existing buffer becomes current.
The *f*, *w*, *e*, and *E* commands do not accept
names for files that are already stored in another buffer.

Be aware that *ed.py* only knows about files that are
loaded into buffers.  It is possible to create a scratch
file with almost any name with the *b* command, and it is
possible to write over almost
any file in the file system from any buffer with the *w* command
or the *f* command.

We recommend avoiding the *e*, *E*, and *f* commands,
and using the *main* buffer only as a scratch buffer.
It is less confusing to use the *B* command instead.
Then you can always save the buffer contents in the
intended file by using the *w* command without arguments.

## Differences from classic ed and sam ##

**ed.py** does not support these classic *ed* commands:
*H h n P u wq W*.

**ed.py** does not support the classic *ed* iteration commands *g G v V*.

**ed.py** does not support the classic *ed* *p* command suffix (for
printing the current line after any command).

**ed.py** supports the *sam* command *n* (print list of buffers),
not the classic *ed* command *n* (print line numbers).
The new *N* command writes the same information into a buffer named *Buffers*.

**ed.py** provides the new *J* command to wrap text in the selected
lines.  The default is dot, the current line.  The selected lines
are wrapped so their length does not exceed *fill_column*, which
defaults to 75 characters, but can be reassigned by including
a parameter to the *J* command, which then remains in effect in that
buffer only until it is reassigned again. The left margin of all the
wrapped lines is the made the same as the left margin of the first line in
the selection.

**ed.py** provides the new *I* and *O* commands to ident and outdent the 
selected lines.  The default is dot, the current line.   The default 
indent and outdent are four spaces, but can be changed by an optional 
integer parameter to either command, which then applies to all subsequent 
indents and outdents until it is reassigned again.

**ed.py** always prints the error message following the *?* character.
There is no way to suppress printing the error messages as in classic
*ed*.

The *@* character can be used to mark a line with the *k@* command, which
can then be located by the *'@* address. In *ed*, only the lower-case
alphabetic characters *a-z* can be used for this (*ed.py* supports *a-z*
also). The *@* mark and the current line, dot, define a *region* or
selection that other commands can use. This region begins with the line
with the *@* mark and includes all the lines up to (but not including) the
current line, dot.

**ed.py** provides the new *[* address range to indicate the region from
mark to dot.

(The *edsel* display editor, which is based on *ed.py*, provides commands  
that set the mark and use the region defined by mark and dot.)

The *e* and *E* commands only work in the *main* buffer.
In *sam*, the *e* command works in any buffer.

The *e* and *E* commands require a filename parameter.
In classic *ed* (and *sam*), *e* with no filename
reloads the current file into the current buffer, which
erases any modifications made since the file was last loaded.

The *B* (and *D*) commands accept only one file (or buffer) name argument,
not multiple names as in *sam*.

In the *s* (substitute) command and in the */text/* and *?text?*
address forms, the text pattern is ordinary text, not a regular
expression.

The *j* (join) command does not save the lines that were joined
in the cut buffer, unlike *GNU ed*.

In the */text/* and *?text?* address forms, **ed.py** only searches
forward to the end of the buffer (or backward to the beginning). It
does not wrap around and continue searching from the beginning (or
end).

The default prompt is the colon *:*, not the empty string.  If no
prompt is desired, the empty string must be requested with *-p ''*
on the command line or *p=''* in the *ed* function call.

The *z* command accepts a negative parameter to scroll backward,
unlike classic *ed*.

## API ##

**ed.py** has a Python API so you can edit from the Python prompt or
write editing scripts in Python.

A convenient way to use the API is to start *ed.py* with the Python *-i*
option as described above, edit some text using *ed* commands, then exit
using the *q* or *Q* command to return to the Python prompt. Then all the
buffer contents that you entered in *ed* are still in memory for you to
work on with the API.

Here is the preceding example expressed using the API.
We import the *ed* module at the Python command, so we have to prefix each
function call with *ed.*

    >>> import ed
    >>> ed.e('test.txt')
    test.txt, 0 lines
    >>> ed.a("""ed.main() enters ed command mode.  By default, the command prompt is :
    ... 'e <name>' loads the named file into the current buffer.
    ... 'a' enters ed input mode and appends the text after the current line.
    ... 'w' writes the buffer contents back to the file
    ... 'q' quits ed command mode.
    ... To quit input mode, type a period by itself at the start of a line.""")
    >>> ed.w()
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

The API also provides a function *process_line* with a single string
argument, which is exactly the command string you would type to *ed*
in command mode or the text string you would type in input mode.  Here
is the preceding example expressed once more using *process_line*:

    >>> import ed
    >>> ed.process_line('e test.txt')
    test.txt, 0 lines
    >>> ed.process_line('a')
    >>> ed.process_line('ed.main() enters ed command mode.  By default, the command prompt is :')
    >>> ed.process_line("'e <name>' loads the named file into the current buffer.")
    >>> ed.process_line("'a' enters ed input mode and appends the text after the current line.")
    >>> ed.process_line("'w' writes the buffer contents back to the file")
    >>> ed.process_line("'q' quits ed command mode.")
    >>> ed.process_line('To quit input mode, type a period by itself at the start of a line.')
    >>> ed.process_line('.')
    >>> ed.process_line('w')
    test.txt, 6 lines

When **ed.py** is running with the [Piety](../piety/README.md)
cooperative multitasking
system, a Piety [Console](../console/README.md) object collects
a command line or input line without
blocking, and then passes that line to *process_line*.

Finally, the API provides the *main* function that runs the application.

## Modules ##

**[ed.py](ed.py)** provides the user interface: the command line and the public
Python API described above.  **ed.py** reads and writes at the
console, but does not directly update buffers or access files.

**ed.py** imports the *buffer.py* module, which provides the
*Buffer* class, which defines the core data structure and the internal
API for updating it.  Many *Buffer* methods correspond to functions in
the API, but here each method has a fixed argument list, provides no
error checking, and no error messages or progress messages.  The
*Buffer* class does not access the console, but updates text buffers
and reads and writes files.

**ed.py** imports the *parse.py* module that provides
functions for parsing *ed* commands, and the
*check.py* module that provides functions for checking
command arguments and supplying default arguments.

**ed.py** imports the *view.py* module, which contains configuration
variables that are read and written by both *ed* and the display
editor *edda*, in order to configure code used by both programs to
run with or without a display.

**ed.py** imports the *Op* display operations enumeration from the
*updates.py* module, which appears in code in *ed* that is also used
by the *edda* display editor.

The *buffer*, *parse*, *check*, *view*, and *updates* modules are
included in this directory.  **ed.py** also uses the Python standard
library modules *re*, *os*, and *sys*.  Other than that, **ed.py** has
no dependencies.

## Data structures ##

The editor data structures are at top level in the *ed.py* module,
so you can easily inspect them at the Python prompt.  The most
important are:

- *current* is the name of the current buffer, a string.

- *buf* is the current buffer, an instance of the *Buffer* class.
  *buf.lines* is the text in the buffer, a list of strings.
  *buf.dot* is the index of the current line in *buf.lines*.

- *buffers* is the collection of all buffers, a dictionary whose keys
  are the buffer names (strings) and whose values are the buffer
  instances.  So *buffers['main'].lines* is the text in the *main* buffer.

In this example we start an *ed.py* session, type a few *ed* commands, then
quit to the Python prompt and type a few statements to inspect the data:

    Begin ed, add a line to the main buffer, and load the ed.md buffer.

    ... $ python3 -im ed
    :a
    Here is a line in main
    .
    :B ed.md
    ed.md, 375 lines
    :1,5p

    ed.py
    =====

    **[ed.py](ed.py)** is a text editor in pure Python inspired by the
    :n
    CRM Buffer            Lines  Mode     File
      * main                  1  Text     None
    .   ed.md               375  Text     ed.md

    Quit to the Python prompt with Q to avoid unsaved changes warning,
    then inspect current, buf, and buffers.

    :Q
    >>> current
    'ed.md'
    >>> buf
    <buffer.Buffer object at 0x10144ee48>
    >>> buffers
    {'main': <buffer.Buffer object at 0x10144eeb8>, 'ed.md': <buffer.Buffer object at 0x10144ee48>}
    >>> buf.lines[:5]
    ['', '\n', 'ed.py\n', '=====\n', '\n']

    You could even update the data structures from the Python prompt, 
    completely bypassing the API.

    >>> buf.lines[3] = '+++++\n'

We started this example by starting *ed.py* from the system command line.
Or, we could start *ed.py* in the Python session with *import ed*
etc., then inspect the data with *ed.current* etc.

Data structures are initialized (to one empty buffer, the *main* buffer)
when the *ed.py* module is imported or reloaded.  But they are *not* reinitialized
when the *main* function is invoked.  This makes it possible to exit and resume
*ed* without losing buffer contents or other context.

## Related programs ##

**ed.py** is at the core of several line editors and display editors.
It provides the command line and text buffers for them all.

**[edo](edo.md)** adds a built-in
Python interpreter and scripting.  This turns *ed.py* into a
minimal but self-contained Python programming environment.

**[edna](edna.py)** wraps *ed.py* (via *edo*) in a [Console](../console/README.md)
object that collects each line without blocking,
so *edna* can run in the cooperative multitasking system,
[Piety](../piety/README.md).  This is necessary for Piety because
*ed.py* runs an event loop that blocks waiting for a complete line
to be entered at the terminal.

**[etty](etty.py)** wraps *ed.py* in a
*Console* object that makes it behave like an old-fashioned teletype
(a printing terminal with limited cursor control).

**[edda](edda.md)** and **[edsel](edsel.md)** are display editors that
use *ed.py* commands.

Revised Jan 2020

