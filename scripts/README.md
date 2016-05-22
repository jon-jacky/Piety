
scripts
=======

Python modules that test and demonstrate the *piety* facilities.  Most
run applications as tasks with a non-blocking *piety* event loop.
Despite the directory name *scripts*, these are all proper Python
modules (with *.py* suffixes and without *#!* lines) that can be
imported, or started with *python -m ...*.  See docstrings (comment
headers) and inline comments in each module for directions and
explanations.

- **console_tasks.py**: Creates a console *Session* instance with three
  *Job* instances: the *pysh* shell, the *ed* line editor, and the *edsel*
  display editor.  The application in each job is a *Command* instance,
  each with its own *reader* method that reads and possibly preprocesses its input. 
  This module is used by the *piety_writers* and *piety_timestamps* scripts.
  It also has a *main* method that
  runs the session in a simple blocking event loop (instead of using
  one of the non-blocking event loops).

- **edc.py**, **edselc.py**: runs the editors *ed.py* and *edsel.py* respectively, using
    the *command* and *key* modules from the *console* directory
    instead of Python *input*, so they read commmand
    lines and input lines one character at a time.  However, they do 
    not use a *piety* event loop, so they still block waiting for the
    next character.

- **edsel_task.py**: runs the display editor *edsel.py* under a
    *piety* event loop, doing non-blocking input with the *command* and
    *key* modules.  Similar to *console_tasks.py*, also uses the
    *Session* and *Job* classes.

- **edsel_timestamps.py**: Uses a blocking event loop to run the *edsel*
    display editor, demonstrating how two *timestamp* generators can 
    write to two editor buffers.

- **embedded.py**: Uses a non-blocking event loop to run the two concurrent file
   writer tasks created by *writer_tasks*, but without an interactive
   interpreter.  Shows that Piety can run in a "headless" mode with no
   console, as is needed in some embedded systems.

- **events.py**: Uses a non-blocking event loop to run two trivial tasks.  
  Demonstrates that Piety can use different event loops, 
  *select/eventloop.py* or *asyncio/eventloop.py*.  Redefine *PYTHONPATH*
  with *bin/paths* or *bin/asyncio_paths* to select an event loop.
  The *embedded* script (above) can also use different event loops.

- **piety_edsel.py**: runs the display editor *edsel.py* under a
    *piety* event loop, doing non-blocking input with the *command* and
    *key* modules.  Similar to *edsel_task.py* but simpler code, 
    uses *Job* without *Session*.

- **piety_timestamps.py**: Uses a non-blocking event loop to run the
  console session with three jobs created by *console_tasks*,
  concurrently with the two timestamp tasks created in this script.
  The timestamp tasks write to editor buffers named *ts1* and *ts2*.
  Display these buffers using the *edsel* display editor commands *b ts1*
  and *b ts2* to see the buffers update as each timestamp is written.

- **piety_writers.py**: Uses a non-blocking event loop to run the console session with
  three jobs created by *console_tasks*, concurrently with the two
  writer tasks created by *writer_tasks*.

- **writer_tasks.py**: Creates writer tasks used by the *embedded.py* and
    *piety_writers.py* scripts.

Revised May 2016
