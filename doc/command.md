
Command
=======

The *command* module contains a skeleton command line application,
including a pure Python non-blocking alternative to *readline*.

The *command* module defines a class *Command*, with a *reader*
method that gets a single character typed at the command keyboard, and
adds it to a command line (usually).  When *reader* gets a line
terminator character, it calls a command function and passes the
command line to it.  The *reader* method also handles some editing
and history functions, like Unix *readline*.

The *reader* method is the console task's handler, that is invoked by
the Piety scheduler.  The Piety scheduler only calls *reader* when
there is a character ready for it to read.  Then the *reader* method
returns after handling each character.  Other tasks' handlers can run
between keystrokes, so entering and editing a command line does not
block other tasks.

There is an optional *reader* argument to the *Command* initializer,
which can accept a custom reader that preprocesses sequences of
characters into multi-character keycodes.  This custom reader (if
present) is called by the *reader* method discussed above.  One such
custom reader is provided by the *key* module's *Key* class.  If this
optional reader argument is omitted, the default reader just handles
one character at a time.

The command function is passed as the *handler*  argument to the *Command*
constructor, so this same class can act as the front end to any
command line application.  The command function can invoke the Python
interpreter itself, so a *Command* instance can act as Piety's Python
shell.

Revised February 2015
