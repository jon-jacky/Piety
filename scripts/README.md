
scripts
=======

This directory contains Python scripts that run applications as tasks
or jobs, with our without the Piety scheduler.  See docstrings
(comment headers) and inline comments in each module for directions
and explanations:

- **console_tasks.py**: Creates a console *Session* instance with three
  *Job* instances: the *pysh* shell, the *ed* line editor, and the *edd*
  display editor.  The application in each job is a *Command* instance,
  each with its own *reader* method that reads and possibly preprocesses its input. 
  This module is used by the *piety* script. 
  It also has a *main* method that
  runs the session in a simple blocking event loop, without the Piety
  scheduler.  

- **console_char_tasks.py**: Like *console_tasks*, but uses the
  *Command* class in the mode where a caller outside the instance
  reads and possibly preprocesses the input and passes it to each
  instance's *handle_key* method.  Used with the *piety.twisted*
  script, and also has its own *main* method to run the session.

- **embedded**: Runs the Piety scheduler with the two concurrent file
   writer tasks created by *writer_tasks*, but without an interactive
   interpreter.  Shows that Piety can run in a "headless" mode with no
   console, as is needed in some embedded systems.

- **piety**: Uses the Piety scheduler to run the console session with
  three jobs created by *console_tasks*, concurrently with the two
  writer tasks created by *writer_tasks*.

- **piety.no_defaults**: Similar to  *piety* script, except it uses different
   syntax to define jobs, with no default arguments.  Does not create
   file writer tasks (but they are easy to create "by hand" in the pysh shell).

- **piety.twisted**: Similar to *piety* script, but uses the Twisted
  *reactor.run* method instead of the Piety scheduler to concurrently
  run the console jobs and writers.  Uses *console_char_tasks* and
  *writer_tasks*.

- **writer_tasks.py**: Creates writer tasks used by the *embedded* and
    *piety* scripts.

Revised April 2015
