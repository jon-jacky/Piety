
wyshka.py
=========

**[wyshka.py](wyshka.py) ** provides any command line application with an enhanced
shell that provides a full Python interpreter as well as all of the
application commands.

For example, the **wyshka** command line shell used by the
*[edo](../editors/edo.py)* editor provides both the *ed* command line
and the *pysh* callable Python interpreter.  This makes it possible to
use the *ed.py* Python API (or any other Python statements) without
exiting the editor.  It works like this in *ed* command line mode:

    :<command>       execute ed <command>
    :!<statement>    push Python <statement> to pysh, return to ed command mode
    .. <statement>   push Python continuation line <statement> to pysh
    :!               switch to Python mode

With *edo*, in *!command*, the *command* is passed to the Python
interpreter, not to the system command shell as in classic *ed*.

The **wyshka** shell works like this in Python mode:

    >> <statement>   push Python <statement> to pysh
    .. <statment>    push Python continuation line <statement> to pysh
    >>:<command>     execute ed <command>, return to pysh interpreter
    >>:              switch to ed command mode

So you can use *:command* to execute an *ed* *command* without exiting
Python.

The *[edo](../editors/edo.py)* editor (explained
[here](../editors/edo.md)) demonstrates how to use *wyshka*.

Revised May 2019

