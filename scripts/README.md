
scripts
=======

Python modules that test and demonstrate *Piety*, especially the
*Task*, *Session*, *Job*, and *Console* classes.  Most modules 
provide a *main* method that runs when the module is invoked from 
the command line.  Some of these
*main* methods run one or more applications as *Piety* tasks, using the
non-blocking event loop in *piety.run*.  Others run
applications in an ordinary *while* loop, and block while waiting for
the next event.

Despite the directory name *scripts*, these are all proper Python
modules (with *.py* suffixes and without *#!* lines) that can be
imported, or started with *python -m* .  

See docstrings (comment headers) and inline comments in each module
for directions and explanations.

- **job.py**: Provides a function to make a console job by
  creating and connecting a *Job* instance and a *Console* instance.
  No *main* method.

- **tasks.py**: Makes a console *Session* instance with
  three jobs: a Python shell, a line editor, and a
  display editor.  Makes all three jobs with *job*.  Runs
  the session in a *while* loop.

- **editor_console0.py**: Makes a console job that runs the display editor
  by connecting a *Job* instance and a *Console* instance, but without
  using *job*.  Runs the job in a *while* loop.

- **editor_console.py**: Makes a console job that runs the display editor
  by  using *job* to connect a *Job* instance and a 
  *Console* instance.  Runs the job in a *while* loop.

- **editor_job.py**: Makes a *Job* instance that runs the display editor 
   in a *while* loop.

- **editor_task.py**: Makes a console job that runs the display editor
  by connecting a *Job* instance and a *Console* instance, but without
  using *job*.  Uses *Task* (not *Session*) to run the job with
  *piety.run*.

- **editor_timestamps.py**: Uses a *while* loop to run the *edsel*
    display editor, demonstrating how two *timestamp* generators can 
    write to two editor buffers.

- **embedded.py**: Uses *piety.run* with two concurrent file
   writer tasks created by *writers*, but without an interactive
   interpreter.  Shows that Piety can run in a "headless" mode with no
   console, as is needed in some embedded systems.

- **events.py**: Uses *piety.run* with two trivial tasks. Demonstrates 
  that Piety can use different event loops,
  *select/eventloop.py* or *asyncio/eventloop.py*.  Redefine
  *PYTHONPATH* with *bin/paths* or *bin/asyncio_paths* to select an
  event loop.  The *embedded* script (above) can also use different
  event loops.

- **run_timestamps.py**: Uses *piety.run* with a
  console *Session* instance to run the three jobs created by *tasks*,
  concurrently with the two timestamp tasks created in this script.
  The timestamp tasks write to editor buffers named *ts1* and *ts2*.
  Display these buffers using the *edsel* display editor commands *b ts1*
  and *b ts2* to see the buffers update as each timestamp is written.

- **run_writers.py**: Uses *piety.run* with a console *Session*
  instance to run the three jobs created by *tasks*, concurrently with
  the two writer tasks created by *writers*.

- **writers.py**: Creates writer tasks used by the *embedded.py* and
    *run_writers.py* scripts.

Revised November 2016
