
eden
====

**eden** is a display editor in pure Python based on the line editor
  [ed.py](ed.md) and the simpler display editor [edsel](edsel.md).

**eden** provides all the functionality of *edsel*, and also adds a display
editing mode
that inserts or deletes printing characters anywhere and uses control characters
to move the cursor and to select, cut, and paste text.

## Running eden ##

**eden** uses the same command line options and arguments as *edsel*,
for example:

    python3 -i -m eden lines20.txt -c 12
    ...

or

    python3 -i
    ...
    >>> from eden import *
    >>> eden('lines20.txt', c=12)
    ...

When *eden* starts up, it resembles *edsel*, with a command prompt in the
scrolling region at the bottom of the terminal window.   You must
use *ed* and *edsel* [commands](ed.txt) to read and write files, and to manage
buffers and windows. You may also use *ed* commands to edit the text.

**eden** adds a command *C* to switch from command mode to display editing mode
(that's capital *C*, case is significant).  In display editing mode you can
insert or delete printing characters anywhere and use control characters
to move the cursor and to select, cut, and paste text.

Display editing mode provides a command
*^Z* (hold down the control key while typing the Z key) that
returns to command mode.  There is also a command *^Q* that enables you
to type and execute a single *ed* or *edsel* command and then return immediately
to display editing mode.  This makes it easy to alternate display editing with
commands.

After typing *^Q* you can type any *ed* line address: a line number, a search string,
or a special character (like *$* for the last line).  Then *eden* will move
the cursor to that line and resume display editing.  Therefore, *^Q* can act
as a search command: type *^Q* then */string/* (or *?string?*) to search forward
(or backward) for *string*.  After that, type *^Q* then *//* (or *??*) to search
forward (or backward) for the same *string*.

## Display Editing Commands ##

At this time, most display editing commands are single control characters
(hold down the control key while typing the named key).  The rest are dedicated
function keys.  We try to use the
same commands as the *emacs* editor when that is possible, but in this version
there are no multi-character commands, and no meta commands
formed by typing the *esc* or *alt* keys.   These are the control key commands:
    
    ^@  set mark, mark (included) to dot (excluded) defines region cut by ^W
    ^space  set mark, like ^@
    ^A  move cursor to start of line
    ^B  move cursor (b)ack one character
    ^D  (d)elete character under cursor
    ^E  move cursor to (e)nd of line
    ^F  move cursor (f)orward one character
    ^H  delete character before cursor
    ^K  delete (kill) line from cursor to end, save in paste buffer
    ^L  refresh screen (useful if screen has become garbled with control characters)
    ^M  open new line below, or break line at cursor
    ^N  move cursor down to (n)ext line
    ^P  move cursor up to to (p)revious line
    ^Q  enter and execute an ed or edsel command, then return to display mode
    ^R  page up
    ^U  delete entire line, save in paste buffer
    ^V  page down
    ^W  delete from mark (included) to dot (excluded), save in paste buffer
    ^X  exchange mark and dot (to show which lines are included)
    ^Y  paste or (y)ank text removed by last ^W, ^K, or ^U, or by *ed* *d* command etc.
    ^Z  exit display editing and return to command mode

These are the dedicated function keys:

    ret  open new line below, or break line at cursor
    bs   delete character before cursor
    del  delete character before cursor
    left (arrow key) move cursor back one character
    right (arrow key) move cursor forward one character
    up   (arrow key) move cursor up to previous line
    down (arrow key) move cursor down to next line

## Editing Commmand Lines ##

It is also possible to edit command lines in the scrolling command region.
These control keys behave the same when editing the command line: *^A ^B ^D
^E ^F ^H ^K*.

These control characters behave differently when editing the command line:

    ^C  interrupt application, write traceback
    ^D  (d)elete character under cursor; if line is empty, exit application
    ^L  redraw line (useful if line has become garbled with control characters)
    ^M  execute command (like ret)
    ^N  retrieve (n)ext line from history
    ^P  retrieve (p)revious line from history
    ^Z  if line is empty, exit application

The *bs del left* and *right* function keys can also be used to edit the command
line.  These function keys  behave differently on the command line:

    ret  execute command line
    up   (arrow key) retrieve previous line from history
    down (arrow key) retrieve next line from history

Commands retrieved from the history
can be edited and submitted.   Command line history including previous
search strings can be accessed during *^Q* commmands.

## Limitations ##

**eden** is *ed.py* underneath.  In display editing mode, you can insert or
delete characters anywhere, but some commands are still line-oriented.

The command to set the mark, *^@* (or *^-space*), only marks the line
(not the character within the line), so the region defined by the mark and
the current line (called dot) is always a sequence of complete lines (that
includes mark but excludes dot).   Therefore, the cut and paste (yank) commands
*^W* and *^Y* always act on a sequence of complete lines.

Search commands only find the line containing the search string.  They
leave the cursor at the beginning of that line, not at the search string
within the line.

Revised Jan 2019

