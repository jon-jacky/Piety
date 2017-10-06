
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

- **editor_job.py**: Makes a *Job* instance that runs a display editor
   in a *while* loop.  Does not use *Console*, uses Python *input*.
   Contrast to *eden* and *run_editor*.

- **editor_timestamps.py**: Demonstrate printing to editor buffers.  Use
     a while loop, not the Piety event loop.

- **embedded.py**: Uses *piety.run* with two concurrent file
   writer tasks created by *writers*, but without an interactive
   interpreter.  Shows that Piety can run in a "headless" mode with no
   console, as is needed in some embedded systems.

- **events.py**: Uses *piety.run* with two trivial tasks. Demonstrates
  that Piety can use different event loops, *select/eventloop.py* or
  *asyncio/eventloop.py*. The *embedded* script (above) can also use
  different event loops.

- **run_editor.py** - Uses *piety_run* to run a display editor
    *Console* instance, without using *Job* or *Session*.  Contrast to
    *eden* and *editor_job*.

- **run_timestamps.py**: Uses *piety.run* to run the three jobs
  created by *session*, concurrently with two timestamp tasks created
  in this script.  The two timestamp tasks can be seen updating editor
  windows at the same time the user edits and updates text in other
  windows or in the scrolling command region.

- **run_writers.py**: Uses *piety.run* to run the three jobs created
    by *session*, concurrently with the two writer tasks created by
    *writers*.

- **session.py**: Creates a *Session* instance with three console
    jobs: a shell, a line editor, and a display editor.  Used by 
    *run_timestamps* and *run_writers*.

- **writers.py**: Creates writer tasks used by *embedded* and
    *run_writers*.

Revised December 2016
