
scripts
=======

This directory contains Python scripts that run applications as tasks
or jobs under the Piety non-blocking event loop.  See docstrings
(comment headers) and inline comments in each module for directions
and explanations:

- **console_tasks.py**: Creates a console *Session* instance with three
  *Job* instances: the *pysh* shell, the *ed* line editor, and the *edd*
  display editor.  The application in each job is a *Command* instance,
  each with its own *reader* method that reads and possibly preprocesses its input. 
  This module is used by the *piety* script. 
  It also has a *main* method that
  runs the session in a simple blocking event loop (instead of using
  the Piety non-blocking event loop).

- **embedded**: Runs non-blocking event loop the two concurrent file
   writer tasks created by *writer_tasks*, but without an interactive
   interpreter.  Shows that Piety can run in a "headless" mode with no
   console, as is needed in some embedded systems.

- **eventloop**: Runs a non-blocking event loop with two trivial tasks.  
  Demonstrates that Piety can use different event loops, the usual 
  *select/eventloop.py* or *twisted/eventloop.py*.  Redefine *PYTHONPATH*
  with *bin/paths* or *bin/twisted_paths* to select an event loop.
  The *embedded* script (above) can also use different event loops.

- **piety**: Uses the Piety non-blocking event loop to run the console session with
  three jobs created by *console_tasks*, concurrently with the two
  writer tasks created by *writer_tasks*.

- **piety.no_defaults**: Similar to  *piety* script, except it uses different
   syntax to define jobs, with no default arguments.  Does not create
   file writer tasks (but they are easy to create "by hand" in the pysh shell).

- **writer_tasks.py**: Creates writer tasks used by the *embedded* and
    *piety* scripts.

Revised May 2015
