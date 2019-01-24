
eden
====

**eden** is a display editor in pure Python based on the line editor
  [ed.py](ed.md) and the simpler display editor [eden.py](eden.md).

**eden** provides all the functionality of *eden*, but also adds a display 
editing mode 
that inserts or deletes printing characters anywhere and uses control characters
to move the cursor and to select, cut, and paste text.

## Running eden ##

**eden** uses the same command line options and arguments as *eden*,
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
use *ed* and *edsel* commands to read and write files, and to manage
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

After typing *^Q* you can type any line address: a line number, a search string,
or a special character (like *$* for the last line).  Then *eden* will move
the cursor to that line and resume display editing.  Therefore, *^Q* can act
as a search command: type *^Q* then */string/* (or *?string?*) to search forward
(or backward) for *string*.  After that, type *^Q* then *//* (or *??*) to search
forward (or backward) for the same *string*.

## Display Editing Commands ##

At this time, all display editing commands are control characters: hold
down the control key while typing the other key.   There are no 'meta' commands
formed by typing the *esc* or *alt* keys.   These are the commands:

  ^A  move cursor to start of line
  ...
  ^Z  return to command mode

The four arrow keys can also be used to move the cursor.

## Editing Commmand Lines ##

The right- and left-arrow keys and these control characters can also be used
in command mode to edit command lines: ^A ^B

The up- and down-arrow arrow keys and the ^N and ^P control characters
can be used in command mode to access command history.  The retrieved commands
can then be edited and submitted.   Command line history can be
accessed during *^Q* commmands.

## Limitations ##

**eden** is *ed.py* underneath.  In display editing mode, you can insert or
delete characters anywhere, but some commands are still line-oriented.  

The command to set the mark, *^@* (or *^-space*), only marks the line
(not the character within the line), so the region defined by the mark and
the current line (called dot) is always a sequence of complete lines (that
includes mark but excludes dot).   Therefore, the cut and paste (yank) commands
*^W* and *^Y* always acts on a sequence of complete lines.

Search commands only find the line containing the search string.  They
leave the cursor at the beginning of that line, not at the search string
within the line.

Revised Jan 2019

