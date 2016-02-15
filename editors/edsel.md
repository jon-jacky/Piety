
edsel
===

**edsel** is a display editor in pure Python based on the line editor
  [ed.py](ed.md).

## Display ##

**edsel** is similar to other multiwindow display editors such as
*emacs*.  It divides its display into two main regions: a scrolling
command region at the bottom, and above it a *frame* that holds one
or more windows that show the contents of editor buffers.  As you
type in text, or type commands in the scrolling region, windows
update to show the current text in the buffers.

The command region behaves like a terminal running *ed*: you type a
command, *edsel* prints the response, and any preceding commands and
responses scroll up until they disappear off the top.  There is a
command to adjust the size of the command region (along with the
frame) to retain more (or fewer) lines.

When *edsel* starts, the frame is filled by one window that shows the
contents of the *main* buffer.  This is the *current window* - the
window that has the keyboard focus.  When an *ed* command changes the
current buffer, the current window updates to display the new current
buffer.  *edsel* updates the current window to ensure that it always
shows the *current line* (also called *dot*) in the current buffer,
where text is inserted and changed.

There is a command to add a new window by splitting the current
window.  Initially both windows show the same contents, both including
the current line in the current buffer.  Only one window remains the
current window.  The cursor (at the text insertion point) only appears
in the current window.  It is possible to have two or more windows viewing
different locations (or the same location) in the same buffer.

There are commands delete windows, and to switch the focus to the next
window, which becomes the new current window.  The previous window
saves its cursor location and its cursor disappears.  The buffer
displayed in the new current window becomes the new current buffer.
The new current window restores its saved cursor location.  This becomes
the new current line, the text insertion point (dot).

Each window has a status line at its bottom that shows the line
numbers of the window's current line in the buffer (dot, where you see
the cursor) and the buffer's last line, the name of the buffer, and
the name of the file where the buffer contents would be written.

## Commands ##

## ed commands ##

**edsel** provides all of the [commands](ed.txt) of *ed*.  Most
updates in *edsel* windows are side effects of *ed* commands as they
move the current line around in the buffer, change buffer contents, or
select a different current buffer.

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

In addition to providing all the *ed* commands, *edsel* provides a
few additional commands for managing windows:

- **o2** creates a new window by spliting the current window. 

- **o1** deletes all windows except the current window. 

- **o** moves the focus to the next window, which becomes the current window.

By default, the *edsel* command region displays just two lines.  This
is usually not enough to show all of the output from some commands,
for example *n* (list buffers).  To change the number of lines at any
time during an editing session, type a Python statement that assigns
the *cmd_h* variable.  For example, to set the region to 8 lines, type
this: *!cmd_h = 8*

When you use the *x* command to execute *ed* commands from a buffer,
you can see window contents update as the commands run.  Each command
echoes in the scrolling command region, followed by a short delay so
you can observe its effect.  The echo and delay can be adjusted or
suppressed by two optional *x* parameters that follow the buffer name:
echo (boolean) and delay (float), which default to *True* and *0.2*
seconds.  So *x sample.ed 0 0* suppresses both echo and delay.

## Running edsel ##

**edsel** can run as a standalone program: *python edsel.py*.  But *edsel*
is intended to run in an interactive python sesson: *import edsel* then
*edsel.main()*.  In that case, you can suspend *edsel* by typing its *q*
command, execute other Python statements, then resume by typing
*edsel.main()* again.  You will find all your buffers and other editor
state as you left it.  (You can also begin a restartable *edsel* session
by the command *python -i edsel.py*.)

The *edsel.main()* function takes one optional positional argument, the
file name, and two optional keyword arguments, *p* the command prompt
string and *h* the number of lines (height) of the scrolling command
region.  Type *edsel.main('test.txt')* to begin editing *test.txt*, as if
you had typed *edsel.main()* and then *e test.txt*.  Type
*edsel.main(p=':')* to use a single colon as the command prompt (the
default prompt is the empty string).  Type *edsel.main(h=8)* to make an eight line
scrolling region.  The argument and options can
appear together, so you can type *edsel.main('test.txt', p=':', h=8)*.

**edsel** can wait for input without blocking, so it can run with a
cooperative multitasking system such as [Piety](../piety/README.md).

Revised February 2016
