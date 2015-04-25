
Command
=======

The *command* module contains a skeleton command line application,
including a pure Python non-blocking alternative to *readline*.

The *command* module defines a class *Command*, an input method
that gets a single character (or a multi-character control sequence)
typed at the command keyboard, and adds it to a command line
(usually).  When the input method gets a line terminator character, it
calls a command function and passes the command line to it.  The input
method also handles some editing and history functions, like Unix
*readline*.

The input method is the console task's handler, that can be invoked by
am event loop, which can be a simple blocking *while*-loop, or a
non-blocking event loop such as the Piety scheduler or the Twisted
reactor.  A non-blocking scheduler such as Piety or Twisted only calls
the input method when there is a character ready for it to read.  Then
the input method returns after handling each character.  Other tasks'
handlers can run between keystrokes, so entering and editing a command
line does not block other tasks.

There are actually two alternative input methods.  In the first
alternative, the input method itself reads characters.  To use this
alternative, call the *reader* method without arguments.  In the
second alternative, a caller (outside the *Command* instance) reads
the characters and passes them to the input method.  To use this
alternative, call the *handle_key* method with one string argument.
Both alternatives are demonstrated in the *command* module's *main*
function.

For the first alternative, the default *reader* method reads one
character at a time.  There is an optional *reader* argument to the
*Command* initializer, which can accept a custom reader that might
read and preprocess sequences of characters into multi-character
control sequences sometimes called *keycodes*.  One such custom reader
is provided by the *key* module's *Key* class.

The command function is passed as the *handler*  argument to the *Command*
constructor, so this same class can act as the front end to any
command line application.  The command function can invoke the Python
interpreter itself, so a *Command* instance can act as Piety's Python
shell.

Revised April 2015
