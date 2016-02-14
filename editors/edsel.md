
edsel
===

**edsel** is a display editor in pure Python based on the line editor
  [ed.py](ed.md).

## Display ##

**edsel** divides its display into two main regions: a scrolling
command region, and a *frame* that shows the contents of editor
buffers.  The command region is at the bottom of the display and the
frame is above it.

The command region behaves like a terminal running *ed*: you type a
command, *edsel* prints the response, and any preceding commands and
responses scroll up.

The frame contains one or more windows that show the contents of
editor buffers.  Each window shows a segment of consecutive lines in
one buffer.  Each window has a status line at its bottom that shows
the line numbers of the window's current line and the buffer's last
line, the name of the buffer, and the name of the file where the
buffer contents would be written.

Different windows can show segments of different buffers, or segments
in the same buffer.  One window is the current window that shows the
segment of the current buffer that includes the current line where
insertions, deletions, and changes are made.  As you type, *edsel*
updates the current window to show each command's effects on the
buffer.

## Commands ##

## ed commands ##

**edsel** provides all of the [commands](ed.txt) of *ed*.  Most
display updates in the current window are side effects of *ed*
commands as they move the current line around in the buffer, change
buffer contents, or select a different buffer.

When you type a command *a*, *i*, or *c* that enters *input mode*,
*edsel* opens a line in the window at the insertion point and puts the
cursor there.  You then type lines of text (as many as you want)
directly into the window (not the command region).  You can edit
within your current line in any way provided by your Python's
*input* (or your local substitute), but you can't edit other lines
(that you have already finished by typing RETURN).  When you are done,
type a period at the start of a line to exit input mode.  Then *edsel*
puts the cursor back in the command region for you to type another
command.

As in *ed*, you can execute any Python statement at the *edsel*
command line by preceding it with the *!* character, for example
*!dir(ed)*.

## edsel commands ##

In addition to supporting all the *ed* commands, *edsel* provides a
few additoonal commands for managing windows:

- **o2** creates a new window by spliting the current window. 

- **o1** deletes all windows except the current window. 

- **o** moves the focus to the next window, which becomes the current window.
  The buffer in that window becomes the current buffer.

## Running edsel ##

**edsel** can run as a standalone program: *python edsel.py*.  But *edsel*
is intended to run in an interactive python sesson: *import edsel* then
*edsel.main()*.  In that case, you can suspend *edsel* by typing its *q*
command, execute other Python statements, then resume by typing
*edsel.main()* again.  You will find all your buffers and other editor
state as you left it.

The *edsel.main()* function takes one optional positional argument, the
file name, and two optional keyword arguments, *p* the command prompt
string and *h* the number of lines (height) of the scrolling command
region.  Type *edsel.main('test.txt')* to begin editing *test.txt*, as if
you had typed *edsel.main()* and then *e test.txt*.  Type
*edsel.main(p=':')* to use a single colon as the command prompt (the
default prompt is the empty string).  Type *edsel.main(h=8)* to make an eight line
scrolling region.  The argument and options can
appear together, so you can type *edsel.main('test.txt', p=':', h=8)*.

By default, the *edsel* scrolling command region displays just two
lines.  But this is usually not enough to show all of the output from
some *edsel* commands, for example *n* (list buffers).  Use the *h*
option (above) to show more lines.  Or, to change the number of lines
at any time during an editing session: *!edsel.cmd_h = 8*.

**edsel** can wait for input without blocking, so it can run with a
cooperative multitasking system such as [Piety](../piety/README.md).

Revised February 2016
