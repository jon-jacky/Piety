
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
cursor there.  You then type lines of text (as many as you want)
directly into the window (not the command region).  You can edit
within your current line in any way provided by your Python's
*raw_input* (or your local substitute), but you can't edit other lines
(that you have already finished by typing RETURN).  When you are done,
type a period at the start of a line to exit input mode.  Then *edd*
puts the cursor back in the command region for you to type another
command.

**edd** provides a few new commands (not in *ed.py*) to make it easy
to move around the buffer (by changing the current line): *Z* pages
forward, *X* pages backward, and *space* moves backward one line.  The
*ed.py* empty command (just type *RETURN*) moves forward one line.

You can execute any Python statement at the *edd* command line by
preceding it with the *!* character, for example *!dir(edd)*.

**edd** can run as a standalone program: *python edd.py*.  But *edd*
is intended to run in an interactive python sesson: *import edd* then
*edd.main()*.  In that case, you can suspend *edd* by typing its *q*
command, execute other Python statements, then resume by typing
*edd.main()* again.  You will find all your buffers and other editor
state as you left it.


The *ed.main()* function takes one optional positional argument, the
file name, and two optional keyword arguments, *p* the command prompt
string and *h* the number of lines (height) of the scrolling command
region.  Type *edd.main('test.txt')* to begin editing *test.txt*, as if
you had typed *edd.main()* and then *e test.txt*.  Type
*edd.main(p=':')* to use a single colon as the command prompt (the
default prompt is the empty string).  Type *edd.main(h=8)* to make an eight line
scrolling region.  The argument and options can
appear together, so you can type *edd.main('test.txt', p=':', h=8)*.

By default, the *edd* scrolling command region displays just two
lines.  But this is usually not enough to show all of the output from
some *edd* commands, for example *n* (list buffers).  Use the *h*
option (above) to show more lines.  Or, to change the number of lines
at any time during an editing session: *!edd.cmd_h = 8*.

**edd** can wait for input without blocking, so it can run with a
cooperative multitasking system such as [Piety](../piety/README.md).

Revised February 2015
