
editors
=======

Text editors

- **README.md**: Directions for using the *sked*, *edsel*, and *dmacs* editors,
  see below.

- **NOTES.txt**: Notes on the code in *sked*, *edsel*, and *dmacs*.

- **HOW.md**: How we program.

- **edsel.py**: Display editor that uses the same commands as *sked*.

- **edselinit.py**: Define and initialize global variables used by *edsel*.

- **dmacs.py**: Invoke editor functions with emacs keycodes.

- **dmacsinit.py**: Define and initialize global variables used by *dmacs*.

- **sked.py**: Line editor inspired by the classic Unix *ed*.

- **skedinit.py**: Define and initialize global variables used by *sked*.


### Introduction ###

The modules here comprise a minimal Python programming environment.
We can have all of our source code, our editors, and the interactive Python
interpreter always available in our Python session. We can write code that
we load and run immediately, without restarting the session or losing
any work in progress. See [how we program](HOW.md).

### sked ###

**sked.py** is the Stone Knife Editor, a line editor inspired by the classic 
Unix editor *ed*.

There is no main program.  Editor commands are just functions defined here,
to call from the Python REPL.

To edit:

    $ python3 -i 
    ...
    >>> import sked
    >>> from sked import *
    >>> e('README.md')
    README.md, 117 lines
    >>> a()
    ...

Here the Python *-i* (interactive) option enables editing on the command
line and also command history.  And, it ensures that if a function 
terminates abnormally for any reason -- including a program crash or 
*^C* interrupt -- 
Python does not exit, but control returns to the Python prompt, and 
all the data in the session remains intact, so you can simply resume working.

Here *from sked import \** imports the
command names from *sked* into the REPL so they can be used without
qualification:
*e(...)* instead of *sked.e(...)*.

The *e* (edit) command loads a file into a buffer in the editor.

The *a* (append) command adds text to the buffer.  Just type lines of 
text on the following lines, each will go into the buffer until you type
a period by itself at the start of a line to exit from the *a* command.

Then other commands can edit in the buffer and print its contents on 
the terminal.

There is no continually updating display that shows the buffer contents.
Editor command output appears in the REPL, then scrolls up as more commands
are typed and executed. You could edit with *sked* on an old printing terminal.

To see all the commands and arguments that are available, read the source, or 
type *help(sked)* in the REPL.  Type *help(e)* (for example) to learn 
about the *e* command, likewise for all the other commands.
Type *dir(sked)* to see just the names of functions and variables.
The commands all have names that are just one or two letters.

To add or change behavior in *sked*, simply edit the module and reload 
it.  Changes are effective immediately, without restarting the Python
session or losing any work in progress.

    ...
    >>> from importlib import reload
    >>> reload(sked)
    ...

The name *sked* is inspired by Kragen Sitaker's Stone Knife Forth.

### edsel ###

**edsel.py** is a display editor that uses the same commands as *sked*.

To edit with *edsel*, first begin *sked* as explained in the previous section.
Then:

    ...
    >>> import edsel
    >>> from edsel import *
    >>> win(24)
    ...

The command names in *edsel* are the same as in *sked*.
Here *from edsel import \** loads the commands from *edsel* into 
the REPL, replacing the commands with the same names imported earlier
from *sked*.

Here *win(24)* opens a display window 24 lines tall at the top of
the same terminal where the Python REPL runs.  This window shows 
the lines in the buffer around the current line, dot.
(24 lines is just an example, it is a good choice when the terminal
is 33 lines tall.)  You can use the *win* command to grow or shrink the 
window at any time, to make more or less room for command output in
the Python REPL.

The Python REPL continues to run and scroll up in the remaining lines
at the bottom of the terminal. 
Here you can type the same editing commands you used in *sked*,
but now the window updates to show the changes in the buffer as
they are made.

When you type *a()* to start the *append* command, the blinking cursor moves
up from the Python REPL to the text insertion point in the window,
and the message *Appending...* replaces the contents of the status line.
Then when you type, each character appears immediately in the window at the 
intended location.  This continues until you type . at the beginning 
of a line to exit append mode.  Then the line with '.' disappears, 
the usual text reappears on the status line, 
and the blinking cursor returns to the Python REPL for the next command.

In append mode, you can edit the line you are entering. 
Thanks to the Python *-i* (interactive) option, 
you can use control keys to move the cursor, insert and delete
characters, and cut and paste words --- but only within that one line.
When you type RETURN, the line is added to the buffer and you cannot
edit it anymore.   The only way to edit a line in the buffer is to call
sked functions at the Python REPL.  You can call 
the *c* (change) function to substitute text in that line.
Or, you can delete the line and append a different one.

Some commands, for example *p()* (print), no longer print output in
the Python REPL because their effects are now visible in the display window.
If you do want to see their output in the python REPL, you can still
run the command in *sked* by prefixing the command name with the 
module name: *sked.p()*.

Help text in *edsel* is cryptic.  To see the more helpful text from *sked*
you must prefix the command name with the module name: *help(sked.e)*.

To finish display editing and return to line editing in *sked*:

    ...
    >>> clr()
    >>> from sked import *
    ...

Here *clr()* dismisses the window by restoring full screen scrolling,
so the window contents soon scroll away at the top of the terminal.
Here *from sked import \** copies the commands in *sked* back into the REPL.
To resume display editing, repeat *from edsel import \** and
*win()* (*win* without an argument restores the previous window size).

The name *edsel* is from the [Edsel](https://en.wikipedia.org/wiki/Edsel)
automobile:
[*it has the new ideas next year's cars are copying!*](https://www.alamy.com/stock-photo-ford-edsel-advert-for-the-1958-model-edsel-convertible-25549787.html?imageid=B9FEB0EB-5F12-45D5-9327-D0BB90416BF1&p=13044&pn=1&searchId=6cb698f459186cbb7fdcfa8a40b23782&searchtype=0)

### dmacs ###

**dmacs.py** is a display editor where you invoke *edsel* functions by 
typing some of the 
[emacs control keys](https://www.gnu.org/software/emacs/refcards/pdf/survival.pdf)
(or key sequences).  When running *dmacs*,
you no longer have to use the Python REPL to edit.  Every *edsel* function 
can be invoked by a keystroke or two.

To run *dmacs*, first start *sked*, then *edsel*, as described above.  Then,

    ...
    >>> import dmacs
    >>> from dmacs import dm
    >>> dm()

After you type *dm()*, the Python prompt does not appear because Python
is busy executing the *dm* function.  Now you can type emacs control keys
to edit.   To exit *dm* and return to the Python prompt, type the control
key *M-x* ("meta x", formed by holding down the ALT key while you type x).
Then the *dm* function returns and the Python prompt reappears.  Now 
you can return to typing *edsel* function calls (or any other Python
statements).  You can type *dm()* again to resume *dmacs*.

To see what control keys are available, see the *keymap* 
dictionary in the *dmacs.py* source code file, which associates 
each key with its function.  Each control
key has the same function in *dmacs* as it does in *emacs*.
(There is one exception: *C-x C-r*, see below.)

There is no control key to enter append mode. Instead, simply type RETURN
at any time while running *dmacs*.  An empty line will open below the
current line and the blinking cursor will appear there.  Now append
mode works just as it does in *sked* and *edsel*: you can
type in any number of lines, editing in the most recent line as you go,
until you type a period at the beginning of line to exit append mode.

When *dmacs* is in append mode, it does not respond to any of its
control keys.  It is easy to enter append mode by mistake by
typing RETURN, or to remain in append mode by forgetting to type the period.
If your session seems unresponsive, try exiting append mode by  typing
RETURN then a period at the beginning of a line.

When you type a key that invokes a function that has a string argument
-- to name a file, buffer, seach string or replacement string --
*dmacs* prompts for it on the line below the status
line.  Type the string and press RETURN.  You can edit the string inline
before you press RETURN.  There is always a default, just press RETURN
to accept it.  To cancel the operation, type '???' by itself, or at
the end of the string, then press RETURN.
(The emacs *C-g* cancel key is not available in *dmacs*.)

Some keys invoke functions that can optionally act on a range of
lines called the *region*.
To define the region, type the key *C-space* (press the control key
and type the space bar).  This sets the *mark*, one end of the region.
Then move the current line *dot* to the other end of the region
(the mark can appear before or after dot in the buffer).
Then type the key to invoke the function.   It will act on 
the lines from *mark* through *dot*, inclusive.
The mark is de-activated after the function executes, so you have 
to set the mark again before each function call that uses it.
When the mark is not activated, those functions only act on the current
line, dot.

You can make changes in any module effective immediately, without
restarting the Python session or losing work in progress.  Just type
*C-x C-r* to invoke *dmacs save_reload*, which writes out the current buffer
to a file and reloads that file as a Python module.

In *dmacs*, as in *sked* and *edsel*, you can only use control keys
to edit within a line when you are entering that line in append mode,
or when you are entering a string in response to a prompt.
To edit a line that has already been added to the buffer, you 
must use the *M-%* key to substitute text in the line.

The only reason to use *M-x* to return to the Python REPL while using
*dmacs* is to view and assign configuration variables, such as
*sked.lmargin* etc.

The name *dmacs* means 'dumb emacs' or maybe 'grade D emacs', barely above
F (fail).

Revised Jun 2023
