
edsel
====

**[edsel](edsel.py)** -- [*it has the new ideas next year's software is copying!*](http://all-classic-ads.com/ford-vintage-ads-1950.html#1958_ford_edsel_advertisement)

**edsel** is a display editor in pure Python.

**edsel** provides all of the commands of the line editors [ed.py](ed.md)
(also [here](ed.txt)) and [edo.py](edo.md) (also [here](edo.txt))  and the
simpler display editor [edda](edda.md) (also [here](edda.txt)).   *edsel*
adds a display  editing mode that inserts or deletes printing characters
anywhere, and  uses display commands bound to control keys to move
the cursor and  to select, cut, and paste text.

**edsel** provides the [wyshka](../shells/wyshka.md) shell 
(also [here](../shells/wyshka.txt)), which provides 
easy access to both  Python and the editor command language, as well as 
redirection and editor scripting.

**edsel** serves as the programmers' user interface to the 
[Piety](../README.md) system.   By providing text editing, a shell and a 
window manager, it comprises a minimal but self-contained
programming environment within a single Python terminal session.

**edsel** is most strongly influenced by
[Emacs](https://www.gnu.org/software/emacs/manual/html_node/emacs/index.html),
and also by [Acme](http://acme.cat-v.org/) and
[Oberon](http://www.projectoberon.com). All three combine an editor, shell,
and tiling window manager.

[Running edsel](#Running-edsel)   
[Using edsel](#Using-edsel)   
[Display editing commands](#Display-editing-commands)   
[Using edsel commands](#Using-edsel-commands)    
[Writing and running Python in edsel](#Writing-and-running-Python-in-edsel)   
[Using the system shell from edsel](#Using-the-system-shell-from-edsel)  
[API and data structures](#API-and-data-structures)   
[Limitations](#Limitations)   

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
program crashes or *C-c* interrupts.  The data for all buffers and
windows remains intact, so you can resume by typing *edsel.main()*.
No function arguments
are needed here, because the data assigned at startup is still present.


## Using edsel ##

When *edsel* starts up, it resembles *edda*, with an editing window at the
top of the terminal window and a command prompt in the scrolling region at
the bottom. Here you can type any *ed*, *edo*, *edda*, or *wyshka*
commands.

**edsel** adds a command *C* to switch from command mode to display
editing mode (that's capital *C*, case is significant).  In display
editing mode you can insert or delete printing characters anywhere and
use control characters to move the cursor and to select, cut, and
paste text.

Display editing mode provides a command *C-z* (*control z*, hold down the
control key while typing the *z* key) that returns to command mode.  There
is also a command *M-x* (*meta x*, hold down the *alt* key while typing
*x*) that enables you to type and run a single
command and then return immediately to display editing mode.  This makes
it easy to alternate display editing with commands.

You will probably use *C-z* and *M-x* frequently while display editing,
because many useful operations are only available in commmand mode.  For
example, you must use [ed commands](ed.txt) to read and write files, and
to manage buffers.

## Display editing commands ##

Most of the display editing commands use the standard
[Emacs key bindings](http://www.math.uh.edu/~bgb/emacs_keys.html).
The *edsel* display editing commands are summarized [here](edsel.txt).

### Display editing in a text window ###

Control keys: *C-f* means hold down the *control* key while typing the *f* key.
*C-f* is sometimes written *^F*. Control keys are case-insensitive; *C-f*
and *C-F* are the same.

    C-@  set mark, mark (included) to dot (excluded) defines region cut by C-w
    C-space  set mark, like C-@
    C-a  move cursor to start of line
    C-b  move cursor (b)ack one character
    C-d  (d)elete character under cursor
    C-e  move cursor to (e)nd of line
    C-f  move cursor (f)orward one character
    C-g  cancel M-x command in progress
    C-h  backspace, delete character before cursor
    C-i  tab, insert spaces
    C-j  run Python statements in region from mark (included) to dot (excluded), append output to current buffer
    C-k  (k)ill line, delete from cursor to end of line, save in paste buffer
    C-l  refresh entire screen
    C-m  return, open new line below, or break line at cursor
    C-n  move cursor down to (n)ext line
    C-p  move cursor up to to (p)revious line
    C-r  search backwards (reverse) for previously entered search string
    C-s  search forwards for previously entered search string
    C-u  discard from start of line to cursor, save in paste buffer
    C-v  move cursor forward one-half page (page down)
    C-w  delete (cut) lines from mark (included) to dot (excluded), save in paste buffer
    C-y  insert (paste or (y)ank) contents last deleted by C-k kill line, C-u discard, M-d kill word, or C-w cut
    C-z  exit display editing and return to command line

Meta keys: *M-q* means hold down *alt* key while typing the *q* key.  Or,
type the *esc* key, then type the *q* key

    M-<  move cursor to beginning of buffer
    M->  move cursor to end of buffer
    M-b  move cursor (b)ackward one word
    M-f  move cursor (f)orward one word
    M-d  kill word, (d)elete word at cursor, save in paste buffer
    M-j  run system shell command in line preceding dot, append output to end of current buffer
    M-q  fill paragraph containing cursor, or immediately preceding cursor
    M-v  move cursor backward one-half page (page up)
    M-x  enter a single command at the command line, return to display editing    
    
*Control-x* prefix keys: First hold down the *control* key while typing *x*,
then type the remaining key.

    C-x 2  create a new window by splitting window in two horizontally
    C-x 1  return to a single window by expanding the current window to fill frame
    C-x o  move to other window

    C-x C-x  exchange mark and dot (move cursor to show where they are)

Special keys on the keyboard:

    return  open new line below, or break line at cursor (same as C-m)
    delete  delete character before cursor (same as C-h)
    backspace  delete character before cursor (same as C-h)
    tab insert spaces (same as C-i)
    left (arrow key) move cursor back one character (same as C-b)
    right (arrow key) move cursor forward one character (same as C-f)
    up (arrow key) move cursor upt to previous line (same as C-p)
    down (arrow key) move cursor down to next line (same as C-n)

### Editing on the command line ###

Some display editing commands also work on the command line, in command
mode. *C-a C-b C-d C-e C-f C-h C-i C-k C-u C-y M-b M-f M-d*  work the same
as above, but these keys work differently on the command line:

    C-c  interrupt application, write traceback
    C-d  if line is empty, exit application.  Otherwise (d)elete character under cursor.
    C-l  refresh command line only (useful if line has become garbled)
    C-m  execute command (like ret)
    C-n  retrieve (n)ext line from history
    C-p  retrieve (p)revious line from history
    C-z  if line is empty, exit application

*delete, backspace, tab, left, right* work the same as in display editing,
but these special keys behave differently in command mode:

    ret  execute command line
    up   (arrow key) retrieve previous line from history (same as C-p)
    down (arrow key) retrieve next line from history (same as C-n)

Commands retrieved from the history can be edited and submitted. Command
line history including previous search strings can be accessed during *M-x*
commmands.

The *edsel* display editing commands are summarized [here](edsel.txt).

## Using edsel commands ##

Most edsel sessions involve both display editing and the command line.
All operations are available at the command line.  Display editing
is often more convienient, but some operations are not available in
display editing.

Regarding the command line: For working with files and buffers see the
instructions for [ed.py](ed.md) (also [here](ed.txt)).  For working with
windows, see [edda](edda.md) (also [here](edda.txt)).  For working with
the built-in Python shell, see [wyshka](../shells/wyshka), and for
editor scripting, see [edo](../editors/edo.md).

The most effective way to use some *edsel* commands is not always obvious.
Here are some hints.

[Search](#Search)  
[Selecting and using the text region](#Selecting-and-using-the-text-region)  
[Selecting and using paragraphs](#Selecting-and-using-paragraphs)  
[Cut and paste](#Cut-and-paste)  
[Indented text](#Indented-text)  
[Wrapped text](#Wrapped-text)  
[Long lines](#Long-lines)  
[Undo](#Undo)  

#### Search ####

After typing *M-x* you can type any *ed* line address: a line number, a
search string, or any other address form (like *$* for the last line).
Then *edsel* will move the cursor to that line and resume display
editing.

Therefore, *M-x* can act as a search command: type *M-x* then
*/string/* (or *?string?*) to search forward (or backward) for
*string*.  After that, when display editing, you can type the commands
*C-s* (or *C-r*) to search forward (or backward) for that same *string*.
The same search string remains in effect in all buffers until you
re-assign it in another */.../* or *?...?* command.

Search commands only find the line containing the search string.  They
leave the cursor at the beginning of that line, not at the search
string within the line.

In *edsel*, search is always case sensitive.

When you use the */.../* and *?...?* forms, the search string is treated
as ordinary text, not a regular expression. You can use these forms to
search for strings that include  regular expression characters such as .
(dot) and * (star) etc. without  escapes, and strings that include invalid
regular expressions such as unmatched parentheses etc.

You can also search for regular expressions.  *edsel* provides the
*|pattern|* and *&pattern&* address forms, where *pattern* is a regular
expression. (Here *|pattern|* uses the pipe character *|* not the 
forward slash character */* used for ordinary text searches.)

#### Selecting and using the text region ####

The text *region* is the target for the *C-w* cut command and
can be used as the selection for any *ed.py* command (that is,
the range of lines affected by the command).

The text *region* is defined by the line called the *mark*  and the 
current line *dot*.  The region is the sequence of complete lines 
beginning with (and including) mark, up to (but *not* including) dot.  

To select a region in display editing mode, put the cursor on the first
line of the region and type  the command to set the mark:  *C-@* (or
*C-space*). The message *Mark set*  appears in the scrolling region at the
bottom of the display. Then move  the cursor (which indicates dot)  down
to the first line after the end of the region. As you move  the cursor,
the end of the region moves also, always following one line behind dot.

To see where the region begins in display editing mode, type *C-x C-x*, which
exchanges dot and mark, so the cursor (which is always at dot) goes to the
line at the beginning of the region.  Then type *C-x C-x* to exchange them
again, so dot and the cursor return to the line after the end of the
region.

You can also select a region in command mode.  Set the mark by using the
*ed k* command  with the *@* label: *k@*.   This is how *ed* (and *edsel*)
represent the mark internally: it has the line address *'@*.  The numerous
*ed* commands that set dot define the other end of the region.

In command mode, the text region defined by mark and dot is selected by
the *[* character and can prefix any command.  For example, *[p* prints
all the lines in the region.   You can select the region in display
editing mode, then apply any *ed.py* command to that region by typing
*M-x*, then at the prompt type *[* then the command.  For example, the
*ed.py* command *[y* copies the region into the cut buffer without
deleting it.  The command *[d* works like *C-w*: it copies the 
region into the cut buffer and deletes it.  After *[d*, *C-y* has the 
same effect as it does after *C-w*: it pastes the deleted region
back into the buffer.   The *[y* command is similar to *[d*, except
it copies the region into the cut buffer without deleting it.

When the region is moved, the mark (as well as other markers set with the 
*ed* *k* command) move with it.   So after cut and paste with
*C-w* and *C-y*, another *C-w* cuts the region that was just pasted.

It is possible for dot to *precede* mark.  This can occur after you type
*C-x C-x* to exchange them.  In this situation, the region comprises exactly
the same lines - but now it begins at dot and extends to the line before
mark.  In display mode, commands that use the region, *C-w* and *C-x C-x*, work
as well when dot precedes mark.

In command mode, the region address range *[* only  works when mark
precedes dot, otherwise *edsel* prints *? address invalid*.

There is no command to delete the mark.  The mark remains until the line
that it indicates is deleted.

#### Selecting and using paragraphs ####

Sometimes you want to perform an operation on the entire paragraph that
contains dot: all the lines up to the nearest preceding empty line, and
down to the nearest following empty line.  Or, if the current line is
empty, you want to operate on the preceding paragraph --- this situation
often arises when you have just finished typing a paragraph.

It is not necessary to set the mark to operate on the current paragraph.
The  *]* address range indicates the current paragraph, even when there is
no mark.

The paragraph range *]* is especially useful with the
wrap, indent, and outdent commands *J*, *I*, and *O*. 

The *M-q* display editing command wraps the current paragraph, so you 
do not have to use command mode for this.

#### Cut and paste ####

The text region is always a sequence of complete lines. Therefore, the cut 
(delete) command *C-w* followed by the paste (yank) command *C-y* always act 
on a sequence of complete lines, inserting the lines before the current 
line.

In contrast to *C-w*, the *kill line* command *C-k* cuts from the cursor to
the end  of the line, discard *C-u* cuts from the beginning of the line to
the cursor, and kill word *M-d* cuts the word at the cursor. A subsequent
*C-y* command pastes that cut segment or word right at the cursor,
anywhere within the same line or a different line.

So the *C-k*, *C-u*, and *M-d* commands have the effect of toggling
subsequent *C-y* commands to inline mode, while *C-w* toggles *C-y* to
multiline mode.

The command mode *x* command is similar to the display mode *yank* *C-y*
command. It also restores the recently cut lines back into the buffer.
But *x* appends the restored lines after dot, then places dot at the last
restored line, while *C-y* restores the lines before dot, and leaves dot
there at the first line after the restored  lines.

The *ed* *yank* (actually *copy*) *y*, *delete* *d*, *substitute* *s*,
and *change* *c* commands all copy text into the cut buffer, from where it
can be pasted by *ed* *x* or edsel *C-y*.

#### Indented text ####

To enter an indented line, type *tab* (or *C-i*) at the beginning of the line.
*edsel* inserts blanks (space characters) to match the indentation of the preceding line.
You can type additional tabs or spaces, or alternatively you may delete some 
preceding spaces, to adjust the indentation differently than the preceding line.
Then type the text of the new indented line.  To enter a sequence of lines with
the same indentation, just type *tab* or *C-i* at the beginning of each line
to match the indentation of the preceding line, then type your text.

To edit an indented line, type *M-f* (jump to next word) at the beginning
of the line. *edsel* places the cursor on the first non-blank character in
the line.  Then edit the text of the indented line.

To indent an existing block of text, use *M-x* to select command mode,
then type *I*, the *ed.py* indent command (capital *I*, the lowercase *i*
is the insert command).  By default *I* just indents the current line, dot,
but you can prefix *I* by any range of line numbers, or any selection
abbreviation.  Type *[I* to indent the text region previously
selected in display mode by a mark command, or *]I* to indent the current
paragraph, any sequence of lines separated from surrounding text by one
or more empty lines preceding and following.  

To outdent a block of text, use the *O* command.

The indent and outdent commands *I* and *O* both take an optional parameter,
the number of spaces to indent (or outdent).   This initially defaults to 
4 spaces, after you type a number, it becomes the default for subsequent
*I* and *O* commands.

#### Wrapped text ####

In display editing mode, use the *M-q* command to wrap text in the
paragraph at the cursor.  The right margin wraps at *text.buf.fill_column*,
which defaults to 75.

Use the *ed.py* *J* command in command mode to wrap text. The selected lines
are wrapped so their length does not exceed *fill_column*, which defaults to 75
characters, but can be reassigned by including a parameter to the *J* command,
which then remains in effect in that buffer until it is reassigned again.

The left margin of all the wrapped lines is the made the same as the left
margin of the first line in the selection.

The default selection for the *J* command is *dot*, the current line.
This is handy for wrapping lines that are too long.

A convenient way to select the lines to wrap is to set the mark at the
beginning of the region, then move the cursor to the line after the region.
Then type *M-x* to get the command prompt, then type the commmand *[J*
which applies the wrap command *J* to the region *[* from mark to dot.
Another convenient way is to simply wrap the current paragraph 
with *]J*, which wraps all the lines up to the nearest
preceding empty line and down the the nearest following empty line.

#### Long lines ####

Lines which are wider than the frame disappear off the right edge of the 
frame (they are *clipped*, not wrapped).  To edit one of these extra-long 
lines, type *M-x* to get the command prompt, then type the command *J* to 
wrap that line to the width defined by the default fill column.  Two or 
more wrapped lines will appear.  You can edit those lines. When you are 
done editing, type a space at the end of each wrapped line, select all the 
wrapped lines and type the *[j* command to join them all into one long line 
again. (If you do not type the extra space at the end of each line, words
will run together where the lines are joined.)

If you type a long line so the end disappears off the right edge, then 
shorten the line by deleting characters in the middle so the following
characters move left again, the characters that were beyond the right
edge do not reappear.  You must use the display editing *refresh* command
*C-l* to make them reappear.  

#### Undo ####

**edsel** has no all-purpose *undo* command.  But it is usually possible
to recover the most recently deleted or altered text.  The command to
restore the text depends on the command that deleted or altered it.

After command mode *delete* *d* or *change* *c*, or display mode *cut*
*C-w*, the deleted lines can be pasted back into the buffer after dot with
command mode *x* or  before dot with display mode *yank* *C-y*.

After *kill line* *C-k*, *discard* *C-u*, or *kill word* *M-d*, the
deleted characters can be pasted back into a line (the original line or
another line) at point by *C-y*.

After *substitute* *s* the original line as it was before the substitution
can be restored at dot, replacing whatever line is there, by *undo* *u*.
Only the last substituted line can be restored.

Only the most recently deleted or altered text can be restored.  *edsel* does
not maintain any history of deletions or alterations before that.


## Writing and running Python in edsel ##

**edsel** is the programmers' user interface to the [Piety](../README.md)
system.   An *edsel* editing session is also an interactive Python
session. You can write and run Python code without exiting *edsel*. 

The *edsel* command line is actually the [wyhska](../shells/wyshka.md)
shell (also [here](../shells/wyshka.txt)), which provides a full Python
interpreter in addition to all of the *edsel* editing commands.

When *edsel* starts up, *wyshka* begins in editor mode, with the editor
command prompt (default *:*).  At this prompt, to use Python, type *!command*.
The *command* string is passed to the Python interpreter, and its output
appears in the scrolling command region.   

If you type a bare *!* without a command, *wyshka* switches to Python REPL
mode, and prints its Python command prompt, *>>* (just two *>* instead of
the three used by standard Python).  Now you can type a series of Python
statements without prefixing each with *!*.  To return to editor mode, 
type *:* at the *>>* prompt.

The *wyshka* shell provides output redirection.  The output of any
Python command (or editor command) can be sent to a text buffer instead of
the scrolling command region.  This is useful when there is too much
output to fit in the command region, or when you want to save the output.

To redirect the output of a Pytjon *command*, use this prefix syntax, where the 
redirection symbol *>* and the  destination buffer name *bufname* precede 
the *command*:  *> bufname !command*

If the named buffer does not yet exist, this command creates it. This
command rewrites the buffer contents, so any contents already in the
buffer are lost.   To preserve the buffer contents and append command output to the end, use
the *>>* redirection symbol instead: *>> bufname !command*

You can select text in any buffer and execute it with Python, using the
*P* command.  For details,  see [edo.md](edo.md).  Any *ed.py* address
range can be used with *P*. For example, a new (or revised) function that
is defined in a paragraph  (a sequence of lines preceded and followed by
blank lines) can be added (or updated) to the Python session.   Place dot
in that paragraph (or in a blank line following it) and type this command:
*]P*.  The Python output appears in the scrolling command region.

You can use any buffer to make a transcript of an interactive Python
session, where all the commands you type and all their output are saved in
the buffer.  The *T* command is similar to *P*, but the Python output
appears at the end of the same buffer.

The *edsel* display editing command *C-j* has the same effect as the *T*
command with no arguments.  It executes the current line in the Python
interpreter and appends any output to the end of the buffer.   Just type
*C-j* after you  enter each Python statement -  there is no need to leave
display editing.   You can use the *C-j* command to make a transcript of a
Python session in a buffer, similar to what you would see in a terminal window.
Just type *C-j* instead of *RET* at the end of each Python statement.

All of the techniques described so far execute the Python code in the
\_\_*main*\_\_ module.   It acts as a sort of scratchpad -- any objects you
create in the \_\_*main*\_\_ module disappear when you exit the Python
session.  For permanent work, you must put your code into a module.
You can create, revise, and run Python modules in *edsel*.

You can edit a module in a buffer, use the editor *w* command to write the
buffer contents to a file.  Then use any of the techniques described above to
run the Python *import* statement or *reload* function to import or reload
that module into the *edsel* session, and then run the code in the module.

Alternatively, you can bypass the file system and simply type the  Python
command *bimport()* or *breload()* to import or reload the module directly
from the current text buffer -- without first writing it out to a file. If
you started  *edsel* by importing it into a Python session with *import
edsel* etc. then you have to type *edsel.bimport()* etc.

## Using the system shell from edsel ##

Our goal is to write and run Python code entirely within an *edsel*
session. Nevertheless, it is sometimes necessary to resort to the host
system shell, for example to navigate the host file system.

In *edsel*, *sh* is a Python function that executes its argument (a string)
with the system shell (*bash*, for example). So it is possible to run
system commands frpm the *edsel* command prompt, for  example *!sh('ls
-l')* (Remember, at the *:* command prompt you have to prefix Python
statements with *!*.)  If you started  *edsel* by importing it into a
Python session with *import edsel* etc. then you have to type
*!edsel.sh('ls -l')*.

The *Z* command executes the current line with the shell (so you do  not
have to surround it with *sh('...')*. The display editing command *M-j*
does the same thing.  The shell command output appears at the end of the
buffer.  You can use the *M-j* command to make a transcript of a shell
command session in a buffer, similar to what you would see in a terminal window.
Just type *M-j* instead of *RET* at the end of each shell command line.

Shell command output usually appears in the scrolling command region.
Alternatively, you can use *wyshka* shell output redirection to save
command output in another buffer. The *Z* command and the *M-j* display
editing command send the shell output to the end of the same buffer.

## API and data structures ##

In *edsel*, the window data structures must be prefixed by the *frame*
module name: *frame.win* is the current window, *frame.windows* is the
list of windows, etc.

If you started *edsel* in an interactive Python session by *import edsel*,
then you must also add *edsel* to the prefix: *edsel.frame.win* etc.
This applies to all the directions here.

In *edsel*, the text data structures must be prefixed by the *text*
module name: *text.buf* is the current buffer, *text.buffers* is the
collection of buffers, etc.  (Or *edsel.text.buf* etc.)

In *edsel*, *ed* data structures and calls to the *ed* API must be prefixed by
the module name *ed.*  For example: *ed.prompt*, *ed.a('append line after dot')*,
etc. (Or *edsel.ed.prompt* etc.)

In *edsel*, calls to the *edda* API require a prefix:
*edda.o(2)*, *edda.h(12)* etc.  (Or *edsel.edda.o(2)* etc.)

This modular structure is the result of how *edsel* was developed. I wrote
a series of editors with increasing functionality: *ed.py* (line editor),
*edo* (adds Python interpreter and scripting), *edda* (adds display, but
still provides only *ed* commands for line editing), and finally *edsel* (adds
display editing at any character position).

Each editor in this sequence imports its predecessor.  The result is a
structure where *edsel* has all its predecessors nested inside, like a
matryoshka doll.  Functionality is spread among *edsel* and all the
imported programs.  To make it a little more convenient, the modules
are all made available at top level in the *edsel* module by these
statements:  *import edda; edo = edda.edo; ed = edo.ed; text = ed.text;
frame = edda.frame* 

## Limitations ##

**edsel** is *ed.py* underneath.  In display editing mode, you can place
the cursor and insert or delete characters anywhere, but most commands
are still line-oriented.

All *ed* commands leave the cursor at the beginning of the line.

Search commands only find the line containing the search string.  They
leave the cursor at the beginning of that line, not at the search
string within the line.

Some display editing commands also leave the cursor at the beginning of
the line.  For example, the *C* command that enters (or re-enters) display
editing mode, the *M-x* command that enters and executes a single command
line, and the *C-x o* command that moves the cursor to the next
window.

When *edsel* puts the cursor at the start of a line, you can 
jump to the position you want by repeating the *M-f*
command that moves the cursor to the beginning of the next word.

As you type and edit characters within a line, *edsel* renders them
directly to the window on the display, but does not yet store them  in the
window's text buffer.   When you type *Return* at the  end of the line, or
move to a different line, then *edsel* stores the completed  line in the
text buffer by calling the *edsel* *store_line* method.   If you have
another window displaying the  same  text buffer, the line you are typing
or editing in the focus window does  not appear in the other window until
you finish editing the line by typing  *Return*, or perform some other
operation that calls *store_line*.

Revised May 2022

