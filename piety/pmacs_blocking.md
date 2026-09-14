 
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

    ...$ python3 -m piety0
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

At this time, we believe we have removed all the blocking code from *pmacs*.

Revised Sep 2026


