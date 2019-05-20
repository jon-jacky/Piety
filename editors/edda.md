
edda
=====

**[edda](edda.py)** is a simple display editor in pure Python.
It is still line- and command-oriented like *ed.py*,
but it also shows buffers update in display windows as
you edit with *ed* commands. *edda* adds a few new commands
for managing display windows.

**edda** is  based on the line editor [ed.py](ed.md).
It also provides the built-in Python shell and scripting provided
by [edo.py](../editors/edo.md).  Those two pages
provide much of what you need to know to use *edda*.

The shell and scripting turn *edda* into a minimal but self-contained
Python programming environment.  It divides the screen
to show one or more editor windows at the top, and a
command interpreter for Python or editor commands at the
bottom.  You can edit modules and
write them out using *ed* cmmands, then use the
Python interpreter to import or reload modules, call their functions,
and inspect and update their data structures.
Or, you can bypass the file system and run
Python scripts directly from editor buffers, or execute Python
statements from selected text in any buffer.

## Running edda ##

**edda** can run as a standalone program or in an interactive Python session.

**edda** is invoked using a similar command line or function call as
[ed.py](ed.md).  It adds one more option, *c*, the number of lines in
the scrolling command region (see below), for example:

    python3 -im edda lines20.txt -c 12
    ... main window appears ...

    lines20.txt, 20 lines
    :

or

    python3 -i
    ...
    >>> import edda
    >>> edda.main('lines20.txt', c=12)
    .... main window appears ...

    lines20.txt, 20 lines
    :

If you use the Python *-i* option, control transfers to an interactive
Python prompt when *edda* stops for any reason.  The data for all buffers and
windows remains intact, so you can resume by typing *edda.main()*.
No function arguments
are needed here, because the data assigned at startup is still present.

## Display ##

**edda** looks similar to other multiwindow display editors such as
*emacs*.  It divides its display into two main regions: a scrolling
command region at the bottom, and above it a *frame* that holds one
or more windows that show the contents of editor buffers.
One of the windows is the *current window* that shows where commands
take effect.  The current window always shows a *cursor* or *marker* that
shows where the next insertion or deletion will take place.

The command region behaves like a terminal running *ed*: you type a
command, *edda* prints the response, and any preceding commands and
responses scroll up until they disappear off the top.
As you type in text, or type commands in the scrolling region, windows
update to show the current text in the buffers.

**edda** imports *[edo](edo.md)*, so it includes the *wyshka* shell
that provides both the *ed* command line and a Python interpreter.
From the Python interpreter, you can
import or reload modules, call their functions,
and inspect and update their data structures.

There is a command to adjust the size of the command region (along with the
frame) to retain more (or fewer) lines.  When using the Python
interpreter, it can be useful to expand the command region to
nearly half the display.

Each window has a status line at its bottom.  Near the left edge of
the status line, a dot indicates this is the current window, a percent sign
indicates that the buffer in the window is read-only, and an asterisk
indicates that the buffer in the window has unsaved changes.   Then the
status line shows the buffer name, the location and line
number of the current line in the buffer, the total number of
lines in the buffer, and perhaps some other information.

## Commands ##

## ed commands ##

**edda** provides all of the [commands](ed.txt) of *ed*.  Most
updates in *edda* windows are side effects of *ed* commands as they
move the current line around in the buffer, change buffer contents, or
select a different current buffer.

When you type a command *a*, *i*, or *c* that enters *input mode*,
*edda* opens a line in the window at the insertion point and puts the
cursor there.  You then type lines of text (as many as you want)
directly into the window (not the command region).  You can edit
within your current line in any way provided by your Python's
*input* (or your local substitute), but you can't edit other lines
(that you have already finished by typing RETURN).  When you are done,
type a period at the start of a line to exit input mode.  Then *edda*
puts the cursor back in the command region for you to type another
command.  A marker remains in the window where the cursor was, to show
where subsequent commands will take effect.

Conventional full-screen display editing is provided by *[edsel](edsel.md)*,
a more capable editor that is based on *edda*.

## Window commands ##

When *edda* starts, the frame is filled by one window that shows the
contents of the *main* buffer.  This is the *current window* - the
window that has the keyboard focus.  When an *ed* command changes the
current buffer, the current window updates to display the new current
buffer.  *edda* updates the current window to ensure that it always
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

By default, the frame is made large enough so the *edda* command region 
displays just two lines.  This
is usually not enough to show all of the output from some commands,
for example *n* (list buffers).  Use the *-c* option to set more lines
when you invoke *edda* (see examples above).  Or, to change the
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
echoes in the scrolling command region, followed by a short delay before
processing the next command so
you have time to observe its effect.  The echo and delay can be adjusted or
suppressed by two optional *X* parameters that follow the buffer name:
echo (boolean) and delay (float), which default to *True* and *0.2*
seconds.  So *X sample.ed 0 0* suppresses both echo and delay,
*X sample.ed 1 1* echoes with a 1 second delay, etc.

## API and data structures ##

The *edda* commands are also available as an API.  The single-letter
command name is the function name and any optional command suffix or
parameter is the command argument.  So the refresh command *L*
becomes the API call *L()*.  The window commands *o* *o1* *o2*
become the API calls *o()* *o(1)* *o(2)*.  The frame balance/resize commands
*h* *h 12* (etc.) become *h()* *h(12)* (etc.).

In *edda*, calls to the *edda* API require no prefix.

In *edda*, the window data structures are in the *frame* module:
*frame.win* is the current window, *frame.windows* is the list
of windows, etc.

In *edda*, calls to the *ed* API must be prefixed by
the module name *ed.*  For example: *ed.a('append line after dot')*.

## Related programs ##

**edda** runs an event loop that blocks waiting for a complete line
to be entered at the terminal.
[desoto](desoto.py) wraps *edda* in a [Console](../console/README.md)
object that collects the line without blocking,
so *desoto* can run in the cooperative multitasking system,
[Piety](../piety/README.md).

**edda** is the core of a more capable display editor, [edsel](edsel.md).

Revised May 2019
