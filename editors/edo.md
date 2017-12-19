
edo.py
======

**edo.py** provides the *[ed.py](ed.md)* line editor with an enhanced
command line shell, provided by the *[wyshka](../shells/wyshka.py)*
module in the *shells* directory.  It also supports a new command *x*
for executing scripts with optional echo and delay, supported by the
*[samysh](../shells/samysh.py)* module in the *shells* directory.

## Enhanced shell ##

The *wyshka* command line shell used by *edo* provides both the *ed*
command line and the *pysh* callable Python interpreter.  This makes
it possible to use the *ed.py* Python API (or any other Python
statements) without exiting the editor.  It works like this in *ed*
command line mode:

    :<command>       execute ed <command>
    :!<statement>    push Python <statement> to pysh, return to ed command mode
    .. <statement>   push Python continuation line <statement> to pysh
    :!               switch to Python mode

With *edo*, in *!command*, the *command* is passed to the Python
interpreter, not to the system command shell as in classic *ed*.

The *wyshka* shell works like this in Python mode:

    >> <statement>   push Python <statement> to pysh
    .. <statment>    push Python continuation line <statement> to pysh
    >>:<command>     execute ed <command>, return to pysh interpreter
    >>:              switch to ed command mode

So you can use *:command* to execute an *ed* *command* without exiting
Python.

## Scripting ##

**edo.py** also adds a new *x* command that executes *ed* commands or
Python statements from an editor buffer, to support scripting and
testing.  (The classic *ed* command *x* prompts for an encryption
key.)

The *x* command requires the buffer name parameter.  It does not make
sense to execute *ed* commands in the same buffer that holds the
script.  The *x* command ignores any line address arguments; it always
executes the entire buffer.  It takes optional parameters *echo*
(boolean) and *delay* (float), which are helpful for visualizing
execution.  The defaults are *echo* *True* and *delay* 0.2 sec.

Revised Dec 2017
