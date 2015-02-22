
Command
=======

The *command* module contains a skeleton command line application.  It
defines a class *Command*, with a *handle_key* method that gets a
single character typed at the command keyboard, and adds it to a
command line (usually).  When *handle_key* gets a line terminator
character, it calls a command function and passes the command line to
it.  The *handle_key* method also handles some editing functions and
other control keys.

The command function is passed as an argument to the *Command*
constructor, so this same class can act as the front end to any
command line application.  The command function can invoke the Python
interpreter itself, so a *Command* instance can act as Piety's Python
shell.

The Command *handle_key* method is usually called by the *getchar*
method in the *key* module.  It is this *getchar* method that is the
console task's handler, that is invoked by the Piety scheduler.

Revised February 2015

