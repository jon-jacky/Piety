
piety
=====

The *piety* script in this directory begins a Piety session by starting
an *asyncio* event loop.  Other scripts demonstrate Piety features 
or start applications.

Piety provides concurrency with a Python *asyncio* event loop.  Tasks 
are implemented by Python *coroutines* or *readers* (event handlers) that
run in an event loop.

Piety provides readers for *pysh*, its custom Python shell, and *pmacs*, its
Emacs-like editor.  These enable the shell and the editor to run without 
blocking in an event loop, so other tasks can run concurrently, as you 
type commands in the shell or edit text in the editor.  You can control
other tasks from the shell and display task output in editor windows.

The *piety* script creates
an event loop named *piety*, adds the readers for the shell and the
editor, and starts the event loop with the shell running.  It also imports
a function *run* which is needed to run other scripts in the event loop.

This directory contains several scripts that start applications or
demonstrate Piety features.  *pmacs_script.py* is the most recent
and shows the most features.

These scripts cannot run standalone.  First 
you must run the *piety* script to start a Piety session, then run the 
script within the session using the *run* function.  For example, to
start the *pmacs* editor: *run('apm.py')*
  
All of these scripts assume you have already assigned *PYTHONPATH* by
running this command:

     . ~/Piety/bin/paths

The initial dot . in this command is essential.  This command assumes 
the top level *Piety* directory is in your home directory.

### Files ###

- **apm.py**: Script to start the *pmacs* editor in an *asyncio* event loop.

- **apmacs.py**: Adapt the *pmacs* editor to run in an *asyncio* event loop.  

- **apyshell.py**: Adapt the *pysh* custom Python shell to run in an *asyncio*
  event loop.
 
- **atimer_script.py**: Demonstrate the Python shell and timer tasks interleaving
  in the Piety event loop.

- **atimer_script.txt**: Explanation and directions for *atimer_script.py*.
 
- **edsel_script.py**: Display interleaving timer tasks in two editor windows.
  Set the timer intervals and stop the tasks from the Python REPL.

- **edsel_script.txt**: Explanation and directions for *edsel_script.py*.

- **piety.py**: Begin a Piety session by starting the *asyncio* event loop.
  Import a function *run* which is needed to run other scripts in the event loop.
  
- **piety.txt**: Explanation and directions for *piety.py*.

- **pmacs_blocking.md**: Explanation and directions for demonstrating
  cooperative multitasking and blocking using *pmacs_script.py*.

- **pmacs_script.md**: Explanation and directions for *pmacs_script.py*.

- **pmacs_script.py**: Edit in one window while a timer task updates the other.
  Set the timer interval, and stop and start timer  tasks from the
  Python REPL.

Revised Aug 2024
 
