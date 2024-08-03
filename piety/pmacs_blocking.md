 
Cooperative multitasking and blocking
=====================================

*pmacs_script.py* can demonstrate some key features of Piety: *cooperative 
multitasking* and an unwelcome potential consequence, *blocking*.

Piety provides concurrency with a Python *asyncio* event loop.  This
provides *cooperative multitasking*.  After an event -- a timeout or a
keystroke -- a task or reader runs code that executes briefly, then exits by
executing *return* or *yield*.  Then the system can respond to another event,
and another task or reader can run. In this way, multiple tasks and readers can
interleave -- if each reader and task cooperates by yielding control
promptly. If any task or reader executes code that runs for a long time, or
*blocks* -- waits for an event that has not yet occurred -- no other tasks
can run, and the system stops responding to events -- the whole session 
is *blocked*.   Tasks and readers that run in an event loop should be coded
so blocking does not occur.

Usually, the *pmacs* editor and the *pysh* shell are *non-blocking*.  Code
that reads input from the keyboard is called from a *reader* that is only
called by the event loop when data is ready, after a key is typed.  
The *piety.add_reader()* call in  *piety.py* sets this up.

Code called from a reader should be non-blocking - it should quickly handle
a single keystroke, then exit.  In contrast,  the Python builtin function
*input*, which reads strings from a sequence of keystrokes that the user
types at the terminal, blocks for the entire time that the user is typing --
or thinking -- until they type *enter* to complete the string.   The standard
library *readline* function blocks in the same way.

It is easy to demonstrate blocking with *pmacs_script.py*.  Just run the
script in the usual way:

    ...$ python3 -m piety
    >>>> run('pmacs_script.py')
    ...

Now the two windows appear, with timer messages appearing in the upper window,
and an editing cursor in the lower window.   Type *M-x* to put the cursor 
at the *>>>>* prompt, and call *input*:

    >>>> input('Input: ')
    Input: 

*input* prints the prompt, and waits for you to type a string.
The messages stop appearing in the timer window.  The session is blocked.
Now type any string at the prompt, then type *enter*.   

    >>>> input('Input: ')
    Input: anything
    'anything'
    >>>> 

The Python interpreter prints the returned value as usual -- it is the
string you  typed -- and messages resume appearing in the timer window.  The
session is unblocked.
 
Most code in *pmacs* and *pysh* avoids calling *input* or *readline*.
Instead, it calls non-blocking functions from our *editline* module, which
each handle one keystroke, building up strings one character at a time.  One
of the reasons we wrote a custom editor and a custom Python shell for Piety is to
ensure that these utilities  are non-blocking, so they can interleave with
other tasks in an event loop.

However, at this time *pmacs* still includes some blocking code.  After you
type *C-s* to enter a search string,, or *C-x b* to switch to another
buffer,  or *C-x C-f* to load a file, *pmacs* prints a prompt, then calls
*input* to read the search string, buffer name, or file name.   The session
blocks while you are typing, until you type *enter* to complete the string, 
or type *???* to cancel the operation.  This is easy to demonstrate
in a *pmacs_script.py* session.  It could be fixed by replacing
that *input* with calls to our *editline* functions.

*pmacs* also blocks when there is a multi-key command, 
such as *C-c >* to indent.   After you type *C-c*, *pmacs* blocks
in a call to *terminal.getchar*, waiting for you to
type *>*.  This is also easy to demonstrate in a *pmacs_script.py*
session.  It could be fixed by exiting fron the reader and returning control
to the event loop after the first key in a multi-key command, instead 
of waiting at *getchar* for the next key.

Revised Aug 2024

