
edo.py
======

**edo.py** provides the *[ed.py](ed.md)* line editor with an enhanced
command line shell, provided by the *[wyshka](../shells/wyshka.py)*
module in the *shells* directory.  It also supports a new command *x*
for executing scripts with optional echo and delay, supported by the
*[samysh](../shells/samysh.py)* module in the *shells* directory.

The enhanced shell and the *x* command are also available in the
applications, modules, and objects that use the *edo* module,
including the *edda* module and the *ed* *Console* job it defines, the
*edsel* display editor application, and the *desoto* module and the
*edsel* *Console* job it defines.

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

Here is a sample session that uses *wyshka* to demonstrate both
the classic *ed* command line and the new *ed.py* Python API:

    Jonathans-MacBook-Pro:editors jon$ python3 -i -m edo
    :!from ed import * # so we can use a() p() etc. without ed. prefix
    :a
    line 1
    line 2
    .
    :p
    line 2
    :1,$p
    line 1
    line 2
    :!a('line A')
    :!p()
    line A
    :!p(1,S())
    line 1
    line 2
    line A
    :!
    >> a("""line B
    .. line C
    .. line D""")
    >> p()
    line D
    >> p(1,S())
    line 1
    line 2
    line A
    line B
    line C
    line D
    >> import datetime
    >> datetime.datetime.now()
    datetime.datetime(2018, 1, 31, 20, 51, 50, 275079)
    >> _.__str__()
    '2018-01-31 20:51:50.275079'
    >> a(_)
    >> p()
    2018-01-31 20:51:50.275079
    >> a(datetime.datetime.now().__str__())
    >> p()
    2018-01-31 20:52:45.504836
    >> :
    :p
    2018-01-31 20:52:45.504836
    :1,$p
    line 1
    line 2
    line A
    line B
    line C
    line D
    2018-01-31 20:51:50.275079
    2018-01-31 20:52:45.504836
    :q
    >>> ^D
    ...$ 

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
