
edd
===

**edd** is a display editor in pure Python based on the line editor
  [ed.py](ed.md).

**edd** divides the display into a window that shows the contents of
the current text buffer, and a command region. The command region
behaves like a console running *ed.py*: you type a command, *edd*
prints the response, and any preceding commands and responses scroll
up.  But also, *edd* updates the window to show the command's effects
on the buffer and the current line.

**edd** provides all of the [commands](ed.txt) of *ed.py*.  There are no *edd*
commands that directly control the display.  All display updates are
side effects of *ed.py* commands as they move the current line around
in the buffer, change buffer contents, or select a different buffer.

When you type a command *a*, *i*, or *c* that enters *input mode*,
*edd* opens a line in the window at the insertion point and puts the
cursor there.  You then type lines of text directly into the window
(not the command region).  You can edit within each line in the usual
way (as provided by *readline*).  When you are done, type a period at
the start of a line to exit input mode.  Then *edd* puts the cursor
back in the command region for you to type the next command.

**edd** provides a few new commands (not in *ed.py*) to make it easy
to move around the buffer (by changing the current line): *Z* pages
forward, *X* pages backward, and *space* moves backward one line.  The
*ed.py* empty command (just type *RETURN*) moves forward one line.

You can execute any Python statement in an *edd* session by preceding
it with the *!* character, for example *!dir(edd)*.

**edd** can run as a standalone program: *python edd.py*.  But *edd*
is intended to run in an interactive python sesson: *import edd* then
*edd.main()*.  In that case, you can suspend *edd* by typing its *q*
command, execute other Python statements, then resume by typing
*edd.main()* again.  You will find all your buffers and other editor
state as you left it.

By default, the *edd* command region displays just two lines.  But
this is usually not enough to show all of the output from some *edd*
commands, for example *n* (list buffers).  It is possible to specify
another size by invoking *edd* with a keyword parameter:
*edd.main(scroll_h=8)*.   You can change the size during an
*edd* session by using the *!* command syntax to assign a new value
to the pertinent variable:  *!edd.cmd_h=8*.

**edd** can wait for input without blocking, so it can run with a
cooperative multitasking system such as [Piety](../piety/README.md).

Revised October 2014

