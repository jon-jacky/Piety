
scripts
=======

Python modules that test and demonstrate *Piety*, especially the
*Task*, *Session*, and *Console* classes.  Most modules
provide a *main* method that runs when the module is invoked from
the command line.  Some of these
*main* methods run one or more applications as *Piety* tasks, using the
non-blocking event loop in *piety.run*.  Others run
applications in an ordinary *while* loop, and block while waiting for
the next event.

Despite the directory name *scripts*, these are all proper Python
modules (with *.py* suffixes and without *#!* lines) that can be
imported, or started with *python -m* .

See *.md* files, docstrings (comment headers), and inline comments in
each module for directions and explanations.

- **background.py**: Demonstrate printing to editor buffers from
     the background.  Use a while loop, not the Piety event loop.

- **demo.md**: Description of *demo.py*.

- **demo.py**: Uses *piety.run* to run the jobs
  created by *session*, concurrently with two timestamp tasks created
  in this script.  The two timestamp tasks can be seen updating editor
  windows at the same time the user edits and updates text in other
  windows or in the scrolling command region.

- **embedded.py**: Uses *piety.run* with two concurrent file
   writer tasks created by *writers*, but without an interactive
   interpreter.  Shows that Piety can run in a "headless" mode with no
   console, as is needed in some embedded systems.

- **events.py**: Uses *piety.run* with two trivial tasks. Demonstrates
  that Piety can use different event loops, *select/eventloop.py* or
  *asyncio/eventloop.py*. The *embedded* script (above) can also use
  different event loops.

- **lines20.txt**: Sample text file for demonstrating editor jobs
  in *session* and *demo*.

- **run_writers.py**: Uses *piety.run* to run the jobs created
    by *session*, concurrently with the two writer tasks created by
    *writers*.

- **session.md**: Description of *session.py*.

- **session.py**: Creates a *Session* instance with four *Console*
    jobs: the *pysh* shell, the *ed* line editor, and the *edda*
    and *edsel* display editors.  Used by *demo* and *run_writers*.

- **writers.py**: Creates writer tasks used by *embedded* and
    *run_writers*.

Revised May 2019
