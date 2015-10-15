
scripts
=======

Python scripts that run applications as tasks or jobs with a
non-blocking event loop. See docstrings (comment headers) and inline
comments in each module for directions and explanations:

- **console_tasks.py**: Creates a console *Session* instance with three
  *Job* instances: the *pysh* shell, the *ed* line editor, and the *edsel*
  display editor.  The application in each job is a *Command* instance,
  each with its own *reader* method that reads and possibly preprocesses its input. 
  This module is used by the *piety* and *piety_timestamps* scripts.
  It also has a *main* method that
  runs the session in a simple blocking event loop (instead of using
  one of the non-blocking event loops).

- **edsel_timestamps**: Uses a blocking event loop to run the *edsel*
    display editor, demonstrating how two *timestamp* generators can 
    write to two editor buffers.

- **embedded**: Uses a non-blocking event loop to run the two concurrent file
   writer tasks created by *writer_tasks*, but without an interactive
   interpreter.  Shows that Piety can run in a "headless" mode with no
   console, as is needed in some embedded systems.

- **eventloop**: Uses a non-blocking event loop to run two trivial tasks.  
  Demonstrates that Piety can use different event loops, 
  *select/eventloop.py* or *asyncio/eventloop.py*.  Redefine *PYTHONPATH*
  with *bin/paths* or *bin/asyncio_paths* to select an event loop.
  The *embedded* script (above) can also use different event loops.

- **piety**: Uses a non-blocking event loop to run the console session with
  three jobs created by *console_tasks*, concurrently with the two
  writer tasks created by *writer_tasks*.

- **piety_timestamps**: Uses a non-blocking event loop to run the
  console session with three jobs created by *console_tasks*,
  concurrently with the two timestamp tasks created in this script.
  The timestamp tasks write to editor buffers named *ts1* and *ts2*.
  Display these buffers using the *edd* display editor commands *b ts1*
  and *b ts2* to see the buffers update as each timestamp is written.

- **writer_tasks.py**: Creates writer tasks used by the *embedded* and
    *piety* scripts.

Revised October 2015
