
eden
====

**[eden](eden.py)** is a display editor in pure Python.

**eden** provides all of the commands of the line editor [ed.py](ed.md) and
the simpler display editor [edsel](edsel.md).
It also provides the built-in Python shell and scripting provided
by [edo.py](../editors/edo.md).
*eden* adds a display editing mode that inserts or deletes printing characters
anywhere, and uses display commands bound to control characters to move the cursor and to
select, cut, and paste text.

The built-in Python shell turns *eden* into a minimal but self-contained
Python programming environment.  *eden* divides the screen
to show one or more editor windows at the top, and a
command interpreter for editor commands or Python at the
bottom.  You can edit modules and write them out, then use the
Python interpreter to import or reload modules, call their functions,
and inspect and update their data structures.

## Running eden ##

**eden** uses the same command line options and arguments as *edsel*,
for example:

    python3 -im eden lines20.txt -c 12
    ...

To start *eden* in a python session, call the method *eden.main*, which
takes the same optional arguments as can appear on the command line:

    python3 -i
    ...
    >>> import eden
    >>> eden.main('lines20.txt', c=12)
    ...

If you use the Python *-i* option, control transfers to an interactive
Python prompt when *eden* stops for any reason.  The data for all buffers and
windows remains intact, so you can resume by typing *eden.main()*.
No function arguments
are needed here, because the data assigned at startup is still present.


## Using eden ##

When *eden* starts up, it resembles *edsel*, with a command prompt in
the scrolling region at the bottom of the terminal window.  You must
use [ed commands](ed.txt) to read and write files, and to manage
buffers. You may also use *ed* commands to edit the text.  You must
used [edsel commands](edsel.txt) to manage windows.

**eden** adds a command *C* to switch from command mode to display
editing mode (that's capital *C*, case is significant).  In display
editing mode you can insert or delete printing characters anywhere and
use control characters to move the cursor and to select, cut, and
paste text.

Display editing mode provides a command *^Z* (hold down the control
key while typing the Z key) that returns to command mode.  There is
also a command *^X* that enables you to type and execute any single
*ed* or *edsel* command and then return immediately to display editing
mode.  This makes it easy to alternate display editing with commands.

## Display Editing Commands ##

Display editing commands are bound to single control characters: hold
down the control key while typing the named key.  Control characters
are case insensitive; *^A* is the same as *^a*.  A few display editing
commands are also bound to dedicated function keys on the keyboard.

These are the control characters, and the display editing commands
bound to them:

    ^@  set mark, mark (included) to dot (excluded) defines region cut by ^W
    ^space  set mark, like ^@
    ^A  move cursor to start of line
    ^B  move cursor (b)ack one character
    ^C  move cursor back one page (page up)
    ^D  (d)elete character under cursor
    ^E  move cursor to (e)nd of line
    ^F  move cursor (f)orward one character
    ^G  cancel ^X command in progress
    ^H  backspace, delete character before cursor
    ^I  tab, insert spaces
    ^J  (j)ump cursor forward to beginning of next word
    ^K  delete (kill) from cursor to end of line, save in paste buffer
    ^L  refresh entire screen (useful after screen is garbled by ^T output etc.)
    ^M  return, open new line below, or break line at cursor
    ^N  move cursor down to (n)ext line
    ^O  move cursor to (o)ther window, next in sequence
    ^P  move cursor up to to (p)revious line
    ^Q  exchange mark and dot (move cursor to show where they are)
    ^R  search backwards (reverse) for previously entered search string
    ^S  search forwards for previously entered search string
    ^T  print task or application status information
    ^U  discard from start of line to cursor, save in paste buffer
    ^V  move cursor forward one page (page down)
    ^W  delete (cut) lines from mark (included) to dot (excluded), save in paste buffer
    ^X  enter and execute ed or edsel command, then return to display mode
    ^Y  insert (paste or (y)ank) contents last deleted by ^K kill, ^U discard, or ^W cut
    ^Z  exit display editing and return to command mode

These are the dedicated function keys and their commands

    return  open new line below, or break line at cursor (same as ^M)
    delete  delete character before cursor (same as ^H)
    backspace  delete character before cursor (same as ^H)
    tab insert spaces (same as ^I)
    left (arrow key) move cursor back one character (same as ^B)
    right (arrow key) move cursor forward one character (same as ^F)
    up   (arrow key) move cursor up to previous line (same as ^P)
    down (arrow key) move cursor down to next line (same as ^N)

## Editing Commmand Lines ##

It is also possible to edit command lines in the scrolling command
region.  These control characters behave the same when editing the
command line: *^A ^B ^D ^E ^F ^H ^I ^J ^K ^T ^U ^Y*.  These function
keys also behave the same on the command line: *bs del left right* and
*tab*.

These control characters behave differently when editing the command line:

    ^C  interrupt application, write traceback
    ^D  if line is empty, exit application.  Otherwise (d)elete character under cursor.
    ^L  refresh command line only (useful if line has become garbled)
    ^M  execute command (like ret)
    ^N  retrieve (n)ext line from history
    ^P  retrieve (p)revious line from history
    ^Z  if line is empty, exit application

These function keys behave differently on the command line:

    ret  execute command line
    up   (arrow key) retrieve previous line from history
    down (arrow key) retrieve next line from history

Commands retrieved from the history can be edited and submitted.
Command line history including previous search strings can be accessed
during *^X* commmands.

## Using eden commands ##

The most effective way to use some *eden* commands is not always obvious.
For working with files and buffers, see the instructions for [ed.py](ed.md)
(also [here](ed.txt)).  For working with windows, see [edsel](edsel.md)
(also [here](edsel.txt)).  For working with the built-in Python shell
and scripting, see [edo](../editors/edo.md).

Here are some hints for using *eden* display commands.

#### Search ####

After typing *^X* you can type any *ed* line address: a line number, a
search string, or any other address form (like *$* for the last line).
Then *eden* will move the cursor to that line and resume display
editing.

Therefore, *^X* can act as a search command: type *^X* then
*/string/* (or *?string?*) to search forward (or backward) for
*string*.  After that, when display editing, you can type the commands
*^S* (or *^R*) to search forward (or backward) for that same *string*.
The same search string remains in effect in all buffers until you
re-assign it in another */.../* or *?...?* command.

In *eden*, search is always case sensitive.

#### Cut and Paste ####

The command to set the mark, *^@* (or *^-space*), only marks the line
(not the character within the line), so the region defined by the mark
and the current line (called dot) is always a sequence of complete
lines (that includes mark but excludes dot).  Therefore, the cut (delete)
command *^W* followed by the paste (yank) command *^Y* always act on a
sequence of complete lines, inserting the lines before the current line.

In contrast to *^W*, the kill *^K* and discard *^U* commands
each cut a segment delimited by the cursor from a
single line, and a subsequent *^Y* command pastes that
same segment right at the cursor, anywhere within the same
line or a different line.

So the *^K* and *^U* commands have the effect of toggling subsequent *^Y*
commands to inline mode, while *^W* toggles *^Y* to multiline mode.

#### Indented text ####

To enter an indented line, type *tab* (or *^I*) at the beginning of the line.
*eden* inserts blanks (space characters) to match the indentation of the preceding line.
The type the text of the new indented line.

To edit an indented line, type *^J* (jump to next word) at the beginning of the line.
*eden* places the cursor on the first non-blank character in the line.  Then edit
the text of the indented line.

## API and data structures ##

In *eden*, calls to the *edsel* API require a prefix:
*edsel.o(2)*, *edsel.h(12)* etc.

In *eden*, the window data structures must be prefixed by the *frame* module name:
*frame.win* is the current window, *frame.windows* is the list
of windows, etc.

In *eden*, *ed* data structures and calls to the *ed* API must be prefixed by
the module name *ed.*  For example: *ed.current*, *ed.a('append line after dot')*,
etc.

## Limitations ##

**eden** is *ed.py* underneath.  In display editing mode, you can place
the cursor and insert or delete characters anywhere, but some commands
are still line-oriented.

All *ed* commands leave the cursor at the beginning of the line.

Search commands only find the line containing the search string.  They
leave the cursor at the beginning of that line, not at the search
string within the line.

Some display editing commands also leave the cursor at the beginning of the
line.  For example, the *C* command that enters (or re-enters) display
editing mode, the *^X* command that enters and executes a single
command line, and the *^O* command that moves the cursor to the next
window.

These limitations might be mitigated somewhat by using the *^J*
command that quickly moves the cursor to the beginning of the next word.

All display editing commands are bound to single control characters.
*eden* does not support sequences of multiple control characters, or
*meta* characters formed by typing the *esc* or *alt* keys.  We have
bound a command to every control character, so no more display editing
commands can be added to *eden*.  Any additional functionality must
be provided at the command line, reached through *^X* or *^Z*.

Revised May 2019

