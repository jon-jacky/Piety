
edsel
=====

**edsel** -- [*it has the new ideas next year's software is copying!*](http://all-classic-ads.com/ford-vintage-ads-1950.html#1958_ford_edsel_advertisement)

**edsel** is a simple display editor in pure Python.
It is still line- and command-oriented like *ed.py*,
but it also shows buffers update in display windows as
you edit with ed commands. *edsel* adds a few new commands
for managing display windows.

**edsel** is  based on the line editor [ed.py](ed.md).
It also provides the built-in Python shell and scripting provided
by [edo.py](../editors/edo.md).  The documentation at those two links
provides most of the information you need to use *edsel*.

**edsel** can wait for input without blocking, so it can run with a
cooperative multitasking system such as [Piety](../piety/README.md).

**edsel** has no dependencies.

We also provide a more capable display editor, [eden](eden.md),
which is based on *edsel*.

## Running edsel ##

**edsel** can run as a standalone program or in an interactive Python session.

**edsel** is invoked using a similar command line or function call as
[ed.py](ed.md).  It adds one more option, *c*, the number of lines in
the scrolling command region (see below), for example:

    python3 -i -m edsel lines20.txt -c 12
    ... main window appears ...

    lines20.txt, 20 lines
    :

or

    python3 -i
    ...
    >>> from edsel import *
    >>> edsel('lines20.txt', c=12)
    .... main window appears ...

    lines20.txt, 20 lines
    :

Use the command *python3 -m edsel -h* to print help.

If you use the Python *-i* option, control transfers to a interactive
Python prompt when *edsel* stops for any reason.  The data for all buffers and
windows remains intact, so you can resume by typing *edsel()*.  No function arguments
are needed here, because the data assigned at startup is still present.

## Display ##

**edsel** looks similar to other multiwindow display editors such as
*emacs*.  It divides its display into two main regions: a scrolling
command region at the bottom, and above it a *frame* that holds one
or more windows that show the contents of editor buffers.
One of the windows is the *current window* that shows where commands
take effect.  The current window always shows a *cursor* or *marker* that
shows where the next insertion or deletion will take place.

The command region behaves like a terminal running *ed*: you type a
command, *edsel* prints the response, and any preceding commands and
responses scroll up until they disappear off the top.  There is a
command to adjust the size of the command region (along with the
frame) to retain more (or fewer) lines.

As you type in text, or type commands in the scrolling region, windows
update to show the current text in the buffers.

Each window has a status line at its bottom.  Near the left edge of
the status line, a dot indicates this is the current window, a percent sign
indicates that the buffer in the window is read-only, and an asterisk 
indicates that the buffer in the window has unsaved changes.   Then the
status line shows the buffer name, the location and line
number of the current line in the buffer, the total number of
lines in the buffer, and perhaps some other information.

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
command.  A marker remains in the window where the cursor was, to show
where subsequent commands will take effect.

Conventional full-screen display editing is provided by *[eden](eden.md)*,
a more complete editor that is based on *edsel*.

**edsel** imports *[edo](edo.md)*, so it includes the *wyshka* shell
that provides both the *ed* command line and a Python interpreter.


## Window commands ##

When *edsel* starts, the frame is filled by one window that shows the
contents of the *main* buffer.  This is the *current window* - the
window that has the keyboard focus.  When an *ed* command changes the
current buffer, the current window updates to display the new current
buffer.  *edsel* updates the current window to ensure that it always
shows the *current line* (also called *dot*) in the current buffer,
where text is inserted and changed.

There are commands to add windows, delete windows, change the
current window, and change window sizes:

- **o2** creates a new window by spliting the current window.  Initially
   both windows show the same contents.  The upper window is the current
   window, where commands can change the current line, dot.  The lower
   window saves the current location of dot and its cursor disappears.

- **o** moves the focus to the next window, which becomes the new
    current window.  The previous window saves its cursor location and
    its cursor disappears.  The buffer displayed in the new current
    window becomes the new current buffer.  The new current window
    restores its saved cursor location.  This becomes the new current
    line, dot.

- **o1** deletes all windows except the current window.

- **h** if there are multiple windows, "balance" them (make them all
    about the same size)

## Frame commands ##

By default, the frame is made large enough so the *edsel* command region 
displays just two lines.  This
is usually not enough to show all of the output from some commands,
for example *n* (list buffers).  Use the *-c* option to set more lines
when you invoke *edsel* (see examples above).  Or, to change the
number command lines at any time during an editing session, use the *h*
command:

- **h** assign number of lines in scrolling command region, in the parameter,
  for example *h 12* to assign 12 lines.  Also, multiple windows (if any)
  are balanced.  If there is no parameter, the *h* command merely balances
  windows.

The *L* command refreshes the entire frame including all windows, and
also the command line in the scrolling region.  This command can be
used to recover if display contents get corrupted or out of synch with
buffer contents.

## Script commands ##

When you use the *X* command to execute *ed* commands from a buffer,
you can see window contents update as the commands run.  Each command
echoes in the scrolling command region, followed by a short delay so
you can observe its effect.  The echo and delay can be adjusted or
suppressed by two optional *X* parameters that follow the buffer name:
echo (boolean) and delay (float), which default to *True* and *0.2*
seconds.  So *X sample.ed 0 0* suppresses both echo and delay.

## Using the *ed* API ##

The ed API is avaiable in edsel by prefixing each call by ed. for example:

    :!ed.a('append line after dot')
    :q
    >>> ed.a('append another line after dot')


Revised Mar 2019
