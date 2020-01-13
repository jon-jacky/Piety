
wyshka.py
=========

**[wyshka.py](wyshka.py)** provides any command line application with an 
enhanced shell that provides a full Python interpreter as well as all of the
application commands.

The *wyshka* shell also provides output redirection.  The output of any
application command or Python command can be sent to a text buffer instead of
the scrolling command region.

## Shell languages ##

The **wyshka** command line shell provides both the application command line
and the *pysh* callable Python interpreter.  This makes it possible to
type and run Python statements without exiting the application.
It works like this in application command line mode:

    :<command>       execute application <command>
    :!<statement>    push Python <statement> to pysh, return to application command mode
    .. <statement>   push Python continuation line <statement> to pysh
    :!               switch to Python mode

In *!command*, the *command* is passed to the Python
interpreter (not to the system command shell as in classic *ed* and
other Unix programs).  
When you type a bare *!* without a command, the command interpreter switches
to the Python REPL, so you can type a series of Python statements without
prefixing each with *!*.

You can type one or more spaces before the *!* character.  Leading
spaces are significant in Python, so any spaces following the *!*
character are considered indentation in the Python statement. 
Usually you should not type any spaces after the *!*.

The **wyshka** shell works like this in Python mode
(the *wyshka* Python prompt is two brackets *>>* to distinguish
it from the standard Python prompt with three brackets *>>>*):

    >> <statement>   push Python <statement> to pysh
    .. <statment>    push Python continuation line <statement> to pysh
    >>:<command>     execute application <command>, return to pysh interpreter
    >>:              switch to application command mode

You can use *:command* to execute an application *command* without exiting
Python.  Type a bare *:*  without a command to switch back to the application
command interpreter.

You can type one or more spaces before the *:* character.  If the application
command interpreter ignores leading spaces, as *ed* does, then you can type
spaces after the *:* also.

Here is a sample session with the *edo* line editor,
which uses *wyshka*, that demonstrates both
the classic *ed* command line and the new *ed.py* Python API.

Start *edo* and use *ed* editing commands to enter some lines of text:

    Jonathans-MacBook-Pro:editors jon$ python3 -im edo
    :a
    line 1
    line 2
    .
    :p
    line 2
    :1,$p
    line 1
    line 2

Use the *ed* Python API at the *ed* command prompt by prefixing each command with *!*

    :!ed.a('line A')
    :!ed.p()
    line A
    :!ed.p(1,ed.S())
    line 1
    line 2
    line A

Switch to the Python prompt by typing *!* alone.  Continue using the *ed* API.

    :!
    >> ed.a("""line B
    .. line C
    .. line D""")
    >> ed.p()
    line D
    >> ed.p(1,ed.S())
    line 1
    line 2
    line A
    line B
    line C
    line D

Use any other Python statements at the Python prompt.

    >> import datetime
    >> datetime.datetime.now()
    datetime.datetime(2018, 1, 31, 20, 51, 50, 275079)

Use Python to compute arguments to the *ed* API.

    >> _.__str__()
    '2018-01-31 20:51:50.275079'
    >> ed.a(_)
    >> ed.p()
    2018-01-31 20:51:50.275079
    >> ed.a(datetime.datetime.now().__str__())
    >> ed.p()
    2018-01-31 20:52:45.504836

To return to the ed command line, type : alone.  The lines that were
added at the Python prompt by using the *ed* API are still in buffer:

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

## Redirection ##

The *wyshka* shell also provides output redirection.  The output of any
application command or Python command can be sent to a text buffer instead of
the scrolling command region.

To redirect the output of *command*, use this prefix syntax, where the 
redirection symbol *>* and the  destination buffer name *bufname* precede 
the *command*:

    > bufname command

Type this after the *wyshka* application command prompt *:*
or the Python command prompt *>>*.  You may type any number of spaces 
before and after the redirection symbol *>*.  You must type at least
one space after *bufname* to separate it from *command*.  In Python mode,
any additional spaces are considered part of the Python command; usually there
shouldn't be any.

If the named buffer does not yet exist, this command creates it.  This
command rewrites the buffer contents, so any contents already in the buffer
are lost.  

To preserve the buffer contents and append *command* output
to the end, use the *>>* redirection symbol instead:
 
    >> bufname command

## Related programs ##

The *wyshka* shell is provided by the *edo* and *edna* line editors,
and the *edda* and *edsel* display editors.

Revised Jan 2020

