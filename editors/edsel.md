
edsel
====

**[edsel](edsel.py)** -- [*it has the new ideas next year's software is copying!*](http://all-classic-ads.com/ford-vintage-ads-1950.html#1958_ford_edsel_advertisement)

**edsel** is a display editor in pure Python.

**edsel** provides all of the commands of the line editor [ed.py](ed.md) 
and the simpler display editor [edda](edda.md).  *edsel* adds a display 
editing mode that inserts or deletes printing characters anywhere, and 
uses display commands bound to control characters to move the cursor and 
to select, cut, and paste text.

**edsel** provides the [wyshka](../shells/wyshka.md) shell, which provides 
easy access to both  Python and the editor command language, as well as 
redirection and scripting.

**edsel** divides the screen
to show one or more editor windows at the top, and a
command interpreter for editor commands or Python at the
bottom.  You can edit modules and write them out, then use the
Python interpreter to import or reload modules, call their functions,
and inspect and update their data structures.
Or, you can bypass the file system and run
Python scripts directly from editor buffers, or execute Python
statements from selected text in any buffer.

**edsel** serves as the programmers' user interface to the 
Piety system.   By providing text editing, a shell and a 
window manager, it comprises a minimal but self-contained Python 
programming environment.

## Running edsel ##

**edsel** uses the same command line options and arguments as *edda*,
for example:

    python3 -im edsel lines20.txt -c 12
    ...

To start *edsel* in a python session, call the method *edsel.main*, which
takes the same optional arguments as can appear on the command line:

    python3 -i
    ...
    >>> import edsel
    >>> edsel.main('lines20.txt', c=12)
    ...

If you use the Python *-i* option, control transfers to an interactive
Python prompt when *edsel* exits or stops for any reason, including 
program crashes or ^C interrupts.  The data for all buffers and
windows remains intact, so you can resume by typing *edsel.main()*.
No function arguments
are needed here, because the data assigned at startup is still present.


## Using edsel ##

When *edsel* starts up, it resembles *edda*, with a command prompt in
the scrolling region at the bottom of the terminal window.  You must
use [ed commands](ed.txt) to read and write files, and to manage
buffers. You may also use *ed* commands to edit the text.  You must
used [edda commands](edda.txt) to manage windows.

**edsel** adds a command *C* to switch from command mode to display
editing mode (that's capital *C*, case is significant).  In display
editing mode you can insert or delete printing characters anywhere and
use control characters to move the cursor and to select, cut, and
paste text.

Display editing mode provides a command *^Z* (hold down the control
key while typing the Z key) that returns to command mode.  There is
also a command *^X* that enables you to type and execute any single
*ed* or *edda* command and then return immediately to display editing
mode.  This makes it easy to alternate display editing with commands.

You will probably use *^Z* and *^X* frequently while display editing, because
many useful operations are only available in commmand mode.  For example,
you must use one of these commands before you can enter a Python command 
or enter the Python shell.

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
    ^L  refresh entire screen
    ^M  return, open new line below, or break line at cursor
    ^N  move cursor down to (n)ext line
    ^O  move cursor to (o)ther window, next in sequence
    ^P  move cursor up to to (p)revious line
    ^Q  exchange mark and dot (move cursor to show where they are)
    ^R  search backwards (reverse) for previously entered search string
    ^S  search forwards for previously entered search string
    ^T  run Python statements from mark (included) to dot (excluded).
    ^U  discard from start of line to cursor, save in paste buffer
    ^V  move cursor forward one page (page down)
    ^W  delete (cut) lines from mark (included) to dot (excluded), save in paste buffer
    ^X  enter and execute ed or edda command, then return to display mode
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
command line: *^A ^B ^D ^E ^F ^H ^I ^J ^K ^U ^Y*.  These function
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

## API and data structures ##

In *edsel*, calls to the *edda* API require a prefix:
*edda.o(2)*, *edda.h(12)* etc.

In *edsel*, the window data structures must be prefixed by the *frame* module name:
*frame.win* is the current window, *frame.windows* is the list
of windows, etc.

In *edsel*, *ed* data structures and calls to the *ed* API must be prefixed by
the module name *ed.*  For example: *ed.current*, *ed.a('append line after dot')*,
etc.

## Using edsel commands ##

The most effective way to use some *edsel* commands is not always obvious.
For working with files and buffers, see the instructions for [ed.py](ed.md)
(also [here](ed.txt)).  For working with windows, see [edda](edda.md)
(also [here](edda.txt)).  For working with the built-in Python shell,
see [wyshka](../shells/wyshka), and for scripting, see [edo](../editors/edo.md).

Here are some hints for using *edsel* display commands.

#### Search ####

After typing *^X* you can type any *ed* line address: a line number, a
search string, or any other address form (like *$* for the last line).
Then *edsel* will move the cursor to that line and resume display
editing.

Therefore, *^X* can act as a search command: type *^X* then
*/string/* (or *?string?*) to search forward (or backward) for
*string*.  After that, when display editing, you can type the commands
*^S* (or *^R*) to search forward (or backward) for that same *string*.
The same search string remains in effect in all buffers until you
re-assign it in another */.../* or *?...?* command.

In *edsel*, search is always case sensitive.

#### Selecting and using the text region ####

The text *region* is the target for the *^W* cut command and
can be used as the selection for any *ed.py* command (that is,
the range of lines affected by the command).

The text *region* is defined by the line called the *mark*  and the 
current line *dot*.  The region is the sequence of complete lines 
beginning with (and including) mark, up to (but *not* including) dot.  To 
select a region, put the cursor on the first line of the region and type 
the command to set the mark:  *^@* (or *^-space*). The message *Mark set* 
appears in the scrolling region at the bottom of the display. Then move 
the cursor (which indicates dot) 
down to the first line after the end of the region. As you move 
the cursor, the end of the region moves also, always following one
line behind dot.

To see where the region begins, type *^Q*, which places the cursor at 
mark, then type *^Q* again to return the cursor to dot, after the end of 
the region.

In command mode, the text region is indicated by the *[* character
and can prefix any command.  For example, *[p* prints all the
lines in the region.   You can select the region in display editing
mode, then apply any *ed.py* command to that region by typing *^X*, then
at the prompt type *[* then the command.  Some useful examples appear 
below.

You might well ask, what if dot *precedes* mark?  ...

You might also ask, how do we get rid of the mark, or cancel the region
so we can start a new one somewhere else?  The *^G* command deletes the mark
and cancels the region.

#### Cut and Paste ####

The text region is always a sequence of complete lines. Therefore, the cut 
(delete) command *^W* followed by the paste (yank) command *^Y* always act 
on a sequence of complete lines, inserting the lines before the current 
line.

In contrast to *^W*, the kill command *^K* cuts from the cursor to the end 
of the line, and *^U* cuts from the beginning of the line to the  cursor. 
A subsequent *^Y* command pastes that cut  segment right at the cursor, 
anywhere within the same line or a different line.

So the *^K* and *^U* commands have the effect of toggling subsequent *^Y*
commands to inline mode, while *^W* toggles *^Y* to multiline mode.

#### Indented text ####

To enter an indented line, type *tab* (or *^I*) at the beginning of the line.
*edsel* inserts blanks (space characters) to match the indentation of the preceding line.
You can type additional tabs or spaces, or alternatively you may delete some 
preceding spaces, to adjust the indentation differently than the preceding line.
Then type the text of the new indented line.  To enter a sequence of lines with
the same indentation, just type *tab* or *^I* at the beginning of each line
to match the indentation of the preceding line, then type your text.

To edit an indented line, type *^J* (jump to next word) at the beginning of the line.
*edsel* places the cursor on the first non-blank character in the line.  Then edit
the text of the indented line.

To indent an existing block of text, use *^X* to select command mode,
then type *I*, the *ed.py* indent command (capital *I*, the lowercase *i*
is the insert command).  By default *I* just indents the current line, dot,
but you can prefix *I* by any range of line numbers, or any selection
abbreviation.  Type *[I* to indent the text region previously
selected in display mode by a mark command.

To outdent a block of text, use the *O* command.

The indent and outdent commands *I* and *O* both take an optional parameter,
the number of spaces to indent (or outdent).   This initially defaults to 
4 spaces, after you type a number, it becomes the default for subsequent
*I* and *O* commands.

#### Wrapped text ####

Use the *ed.py* *J* command in command mode to wrap text. The selected lines
are wrapped so their length does not exceed *fill_column*, which defaults to 75
characters, but can be reassigned by including a parameter to the *J* command,
which then remains in effect in that buffer only until it is reassigned again.

The left margin of all the wrapped lines is the made the same as the left
margin of the first line in the selection.

The default selection for the *J* command is *dot*, the current line.

A convenient way to select the lines to wrap is to set the mark at the
beginning of the region, then move the cursor to the line after the region.
Then type *^X* to get the command prompt, then type the commmand *[J*
which applies the wrap command *J* to the region *[* from mark to dot.

#### Long lines ####

Lines which are wider than the frame disappear off the right edge of the
frame (they are *clipped*, not wrapped).  To edit one of these extra-long
lines, type *^X* to get the command prompt, then type the command *J* to
wrap that line to the width defined by the default fill column.  Two or
more wrapped lines will appear.  You can edit those lines. When you are done
editing, select all the wrapped lines and type the *j* command to join them
all into one long line again.

## Limitations ##

**edsel** is *ed.py* underneath.  In display editing mode, you can place
the cursor and insert or delete characters anywhere, but most commands
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

When *edsel* puts the cursor at the start of a line, you can 
jump to the position you want by repeating the *^J*
command that moves the cursor to the beginning of the next word.

As you type and edit characters within a line, *edsel* renders them 
directly to the focus window on the display, but does not yet store them 
in the focus window's text buffer.   When you type *Return* at the 
end of the line, or move to a different line, then *edsel* stores the completed 
line in the text buffer.   If you have another window displaying the  same 
text buffer, the line you are typing or editing in the focus window does 
not appear in the other window until you finish editing the line by typing 
*Return*, or move to a different line and then do some command that updates
the display.  Just moving to a different line does not update the display,
in order to avoid too many updates.

All display editing commands are bound to single control characters.
*edsel* does not support sequences of multiple control characters, or
*meta* characters formed by typing the *esc* or *alt* keys.  We have
bound a command to every control character, so no more display editing
commands can be added to *edsel*.  Any additional functionality must
be provided at the command line, reached through *^X* or *^Z*.

Revised Mar 2020

