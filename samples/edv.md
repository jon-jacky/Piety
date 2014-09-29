
edv
===

**edv** is a display editor based on the line editor [ed](ed.md).

**edv** can run as a standalone program: *python edv.py*.  But *edv*
is intended to run in an interactive python sesson: *import edv* then
*edv.main()*.  In that case, you can suspend *edv* by typing its *q*
command, execute other Python statements, then resume by typing
*edv.main()* again.  You will find all your buffers and other editor
state as you left it.

**edv** divides the display into regions: a window that shows the
contents of the current text buffer, and a command region. The command
region behaves like a console running *ed*: you type a command, *edv*
prints the response, and any preceding commands and responses scroll
up.  But also, *edv* updates the window to show the command's effects
on the buffer and the current line, called *dot*.

**edv** provides all of the commands of the line editor *ed*.  There
are no *edv* commands that directly control the display.  All
display updates are side effects of *ed* commands as they move dot
around in the buffer, change buffer contents, or select a different
buffer.

**edv** provides a few new commands (not in *ed*) to make it easy to
move around the buffer (by changing dot).  *Z* pages forward, *X*
pages backward, and *space* moves backward one line.

You can execute any Python statement in an *edv* session by preceding
it with the *!* character, for example *!dir(edv)*.

By default, the *edv* command region displays just two lines.  But
this is usually not enough to show all of the output from some *edv*
commands, for example *n* (list buffers).  It is possible to specify
another size by invoking *edv* with a keyword parameter:
*edv.main(scroll_h=8)*.   You can even change the size during an
*edv* session by using the *!* command syntax to assign a new value
to the pertinent variable:  *!edv.cmd_h=8*.

**edv** can wait for input without blocking, so it can run with a
cooperative multitasking system such as [Piety](../piety/README.md).

Revised September 2014

