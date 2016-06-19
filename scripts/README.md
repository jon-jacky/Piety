
scripts
=======

Python modules that test and demonstrate *Piety*, especially the
*Task*, *Session*, *Job*, and *Command* classes.  Some of these
modules run one or more applications as *Piety* tasks, using the
non-blocking event loop in *piety.run*.  Other modules run
applications in an ordinary *while* loop, and block while waiting for
the next event.

Despite the directory name *scripts*, these are all proper Python
modules (with *.py* suffixes and without *#!* lines) that can be
imported, or started with *python -m* .  

See docstrings (comment headers) and inline comments in each module
for directions and explanations.

- **console_job.py**: Provides a function to make a console job by
  creating and connecting a *Job* instance and a *Command* instance.
  No *main* method.

- **console_tasks.py**: Makes a console *Session* instance with
  three jobs: the *pysh* shell, the *ed* line editor, and the *edsel*
  display editor.  Makes all three jobs with *console_job*.  Runs
  the session in a *while* loop.

- **ed_cmd_job.py**, **edsel_cmd_job.py**: Makes a console job that runs the editor *ed*
  (or *edsel*) by connecting a *Job* instance and a *Command* instance, but without
  using *console_job*.  Runs the job in a *while* loop.

- **ed_command.py**, **edsel_command.py**: Makes a *Command* instance
  that runs the editor *ed* (or *(edsel*) in a *while* loop.

- **edsel_console_job.py**: Makes a console job that runs the editor *ed*
  (or *edsel*) by  using *console_job* to connect a *Job* instance and a 
  *Command* instance.  Runs the job in a *while* loop.

- **edsel_job.py**: Makes a *Job* instance that runs the editor *edsel* 
   in a *while* loop.

- **edsel_task.py**: Makes a console job that runs the editor *edsel*
  by connecting a *Job* instance and a *Command* instance, but without
  using *console_job*.  Uses *Task* (not *Session*) to run the job with
  *piety.run*.

- **edsel_timestamps.py**: Uses a *while* loop to run the *edsel*
    display editor, demonstrating how two *timestamp* generators can 
    write to two editor buffers.

- **embedded.py**: Uses *piety.run* with two concurrent file
   writer tasks created by *writer_tasks*, but without an interactive
   interpreter.  Shows that Piety can run in a "headless" mode with no
   console, as is needed in some embedded systems.

- **events.py**: Uses *piety.run* with two trivial tasks.  
  Demonstrates that Piety can use different event loops, 
  *select/eventloop.py* or *asyncio/eventloop.py*.  Redefine *PYTHONPATH*
  with *bin/paths* or *bin/asyncio_paths* to select an event loop.
  The *embedded* script (above) can also use different event loops.

- **piety_timestamps.py**: Uses *piety.run* with a
  console *Session* instance to run the three jobs created by *console_tasks*,
  concurrently with the two timestamp tasks created in this script.
  The timestamp tasks write to editor buffers named *ts1* and *ts2*.
  Display these buffers using the *edsel* display editor commands *b ts1*
  and *b ts2* to see the buffers update as each timestamp is written.

- **piety_writers.py**: Uses *piety.run* with a console *Session* instance to run the
  three jobs created by *console_tasks*, concurrently with the two
  writer tasks created by *writer_tasks*.

- **pysh_command.py**: Makes a *Command* instance
  that runs the *pysh* Python shell in a *while* loop.

- **writer_tasks.py**: Creates writer tasks used by the *embedded.py* and
    *piety_writers.py* scripts.

Revised June 2016
