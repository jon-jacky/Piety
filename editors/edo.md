
edo.py
======

**[edo.py](edo.py)** provides the *[ed.py](ed.md)* line editor with an enhanced
command line shell, including a Python interpreter
provided by the *[wyshka](../shells/wyshka.md)* module.  *edo* also
provides editor commands for running Python code from
selected text in any buffer, functions for importing or reloading
a Python module directly from a buffer, and a function to execute 
system shell commands (with *bash*, for example).

This shell and these commands
turn *ed.py* into a minimal but self-contained
Python programming environment.  In *edo*, you can edit modules and
write them out using *ed* commands, then use the built-in
Python interpreter to import or reload modules, call their functions,
and inspect and update their data structures.
Or, you can bypass the file system and run Python
statements from selected text in a buffer, or import or reload an entire
module from a buffer.

**edo.py** also provides a new command *X*
for executing scripts of editor commands
from an editor buffer with optional echo and delay,
supported by the *[samysh](../shells/samysh.py)* module.
The *X* command is provided for testing *ed.py* itself, as well as the
several other programs built on it (see below).  The echo and delay make
it easy to see the effect of each command in the script.  This is
especially useful for testing the display editors based on *ed.py*.

[Running and resuming edo.py](#Running-and-resuming-edo.py)  
[Wyshka-shell](#Wyshka-hell)  
[Running Python code](#Running-Python-code)  
[Importing and reloading Python modules](#Importing-and-reloading-Python-modules)  
[Using the system shell](#Using-the-system-shell)  
[Editor scripting](#Editor-scripting)  
[Modules](#Modules)  
[API and Data Structures](#API-and-Data-Structures)  
[Related programs](#Related-programs)  

## Running and resuming edo.py ##

You run *edo* just like *ed.py*.  From the system command line:

    python3 -im edo

From a Python session:

    $ python3 -i
    ...
    >>> import edo
    >>> edo.main()

*edo* takes the same command line arguments and *main* function arguments
as *ed.py*.

If you start the Python session with the *-i* option, control returns to the
Python prompt when *edo* exits for any reason.  Then you can resume your
*edo* session just where you left off, with all buffers intact, just by
calling *main()* (or *edo.main()*) at the Python prompt.

## Wyshka shell ##

The [wyshka](../shells/wyshka.md) command line shell used by *edo*
provides both the *ed* command line and the *pysh* callable Python
interpreter.  This makes it possible to use the *ed.py* Python API (or any
other Python statements) without exiting the editor.

The *wyshka* shell also provides output redirection.  The output of any
*ed* or Python command can be sent to a text buffer instead of
the scrolling command region.

## Running Python code ##

In addition to providing a Python shell, **edo.py** also provides new editor
commands for running Python out of text buffers. These commands execute the code
at top level (in the *main* module), they do not import the buffer as a module.

- *P*: Execute selected lines using the *push* method from Python *code* module
*InteractiveConsole* class. The selected lines can be a single line or range of
lines indentified by one or two *ed* line addresses. Default is *dot*, the
current line.

- *R*: Execute selected lines using the builtin *exec* function.

- *T*: Execute selected lines using the *push* method, append output 
to the end of buffer.  

We provide both *P* and *R* commands because the behavior of *push* and *exec*
are different. *P* treats the lines of code the same as the interactive Python
interpreter. It prints the values of expressions even without any explicit
*print* calls, but it requires that the code be formatted with a blank line
preceding every *outdent* (a line with less indentation than its predecessor).
An outdent that is not preceded with a blank line is reported as a syntax
error, and the code is not executed. *R* uses builtin *exec* which runs the
code instead of reporting an error. It runs any valid Python code, but does not
print the values of expressions it evaluates unless there is an explicity
*print* call.

The *P* and *R* commands print any output from the Python code in the
scrolling command region.   The *T* command prints the output at the end
of the buffer (the same buffer containing the code) even if the selected
code is not at the end of the buffer.  

If the Python code crashes, the *P* and *T* commands print any traceback
etc. in the scrolling command region; the *R* command causes the whole
session  to crash.

The *T* command, after it prints the output from the selected Python code
at the end of the buffer, also adds a new empty line to end of buffer
and sets mark and dot there.  Then new lines typed at the end of the buffer
advance dot but leave the mark, so all text typed after the last Python output
is in the selection region, ready to be executed by *]T*.   The *edsel* *^T*
command invokes *edo* *T*.  These turn any buffer into a Python REPL.

There are some inconveniences with *T*.  Error output still appears in the
scrolling region, not the buffer.  Some Python output appears in very long
lines that are not automatically wrapped.

## Importing and reloading Python modules ##

**edo.py** provides Python functions to import or reload a module directly
from  a text buffer, so it is not necessary to save the buffer contents to
a file first:

- *bimport()* imports the current buffer

- *breload()* reloads the current buffer

These function calls can be typed at the *wyshka* shell, like any other
Python statements.

## Using the system shell ##

**edo.py** provides the Python function *sh()* which executes its argument
(a string) with the system shell (*bash*, for example). So it is possible
to run system commands without leaving *edo*, for  example *sh('ls -l')*

Like any other command, shell command output usually appears in the
scrolling command region, but you can use the output redirection
capability of the  *wyshka* shell to save output in a buffer,  for example
to save the output from *ls -l* in the buffer *ls.log*, use this command:
*> ls.log !sh('ls -l')* Here the *!* preceding *sh* indicates that *sh*
and what follows is a *Python* function call, not an editor command
(this is only necessary if *wyshka* is not already in Python mode).

## Editor scripting ##

**edo.py** adds a new *X* command that executes *ed* commands
from an editor buffer, to support scripting and
testing.  (That is an uppercase *X*.  The *ed.py* lower case *x*
command is different.  It pastes recently copied or deleted lines into
the current text buffer).
This command is provided for testing *ed.py* itself , as well as the
several other programs built on it.

The *X* command requires the buffer name parameter (it does not make
sense to execute *ed* commands in the same buffer that holds the
script).
The *X* command ignores any line address arguments; it always
executes the entire buffer.

The *X* command takes optional parameters *echo*
(boolean) and *delay* (float), which are helpful for seeing the
effects of each command in the script; they are especially useful
for testing the display editors based on *edo*.
The defaults are *echo* *True* and *delay* 0.2 sec.

Here is a sample that uses the *X* command to execute the *sample.ed*
script in the *test/ed* directory.  That is the default directory in
this sample.   First, we load the script into an
editor buffer: *B sample.ed*.
Then, we change back to the *main* buffer with *b main* and
execute the test in that buffer with the *X* command: *X sample.ed*.
Each command echoes as it executes, then there is a short delay before
the next command so you can see its effect. The echo and delay can be
adjusted or suppressed by two optional *X* parameters that follow the
buffer name: *X sample.ed 0 0* suppresses both echo and delay.  For example,
in the *test/ed* directory:

    ... $ python3 -im edo
    :B sample.ed
    sample.ed, 18 lines
    :b main
    .   main                 0  None
    :X sample.ed 1 2
    ...
    ... sample.ed executes, echoes commands, waits 2 sec after each command
    ...
    :q
    >>> ^D
    ... $

After the script finishes, you can type *q* at the prompt to exit the editor,
then exit from Python.

In the X command, the buffer name can be abbreviated by providing a prefix
followed by a hyphen -- a sort of "poor person's tab completion".  For
example, the command *X samp-* or even *X s-* might run the test script in
*sample.ed*.  If more than one buffer name begins with the same
prefix, the command just chooses one.

## Modules ##

**[edo.py](edo.py)** imports *ed.py*, so it uses all the modules *ed.py*
imports.  It defines the abbreviation *text* for *ed.text*, the *text* module,
so *text* can be used without the *ed* prefix.

**edo.py** also imports *wyshka.py* and *samysh.py* from the *shells* directory.

## API and Data Structures ##

You can access the editor API and data structures from the Python prompt
via the imported *ed* module.

If you start *edo* at the system command line, *ed.a* is the append function,
*text.current* is the name of the current buffer, *text.buf* is the
current buffer object, and *text.buffers* is the dictionary of buffers
indexed by name.

If you import *edo* into a Python session, then you use *edo.ed.a*,
*edo.text.current* etc.

## Related programs ##

**edo.py** is at the core of several line editors and display editors.
It provides the Python interpreter and scripting for them all.
And, via its imported *ed.py*, it also provides their command lines
and text buffers.

**[edna](edna.py)** wraps *edo.py* in a [Console](../console/README.md)
object that collects each line without blocking,
so *edna* can run in the cooperative multitasking system,
[Piety](../piety/README.md).  This is necessary for Piety because
*edo.py* runs an event loop that blocks waiting for a complete line
to be entered at the terminal.

The **[edda](edda.md)** display editor imports *edo.py*.

The **[edsel](edsel.md)** display editor imports *edda* which imports *edo*.

Revised Apr 2021

