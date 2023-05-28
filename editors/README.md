
editors
=======

Text editors

- **edsel.py**: Display editor that uses the same commands as *sked*.

- **edselinit.py**: Define and initialize global variables used by *edsel*.

- **pmacs.py**: Invoke editor functions with emacs keycodes.

- **sked.py**: Line editor inspired by the classic Unix *ed*.

- **skedinit.py**: Define and initialize global variables used by *sked*.

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

When you type *a()* to start the *append* command, the cursor moves
up from the Python REPL to the text insertion point in the window.
Then when you type, each character appears immediately in the window at the 
intended location.  This continues until you type . at the beginning 
of a line to exit append mode.  Then the line with '.' disappears 
and the cursor returns to the Python REPL for the next command.

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

Revised May 2023
