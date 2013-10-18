
Piety bin directory
=====================

This directory contains commands (shell scripts) and Python programs
for running Piety on a Unix-like host operating system, including
Linux and Mac OS X.

To conveniently use Piety, this directory should be on your execution
*PATH*.  Or, its contents should be installed in some directory that
is on your execution *PATH*.  See *piety_paths* in this directory.

The commands are:
  
- **piety_paths**: assigns paths for running Piety.  .  To prepare to
 use Piety, execute this script, or put the commands from this script
 into your *.profile* or *.bashrc*.  These commands add *Piety/bin* to
 the execution *PATH*, and adds *Piety/piety* and *Piety/samples* to
 the *PYTHONPATH*.

- **piety**: run a Piety session.  Start Python, import the essential
  Piety modules, and start a single console task running a Python
  interpreter.  If you exit from Piety or interrupt it, you will still
  be in Python and can resume Piety with r().

- **piety_writers**: similar to the *piety* command, but also starts
    with two writer tasks defined (but only one running).

The programs are:

- **run_piety**: start Piety with Python shell running.  Invoked by
    the *piety* command.  But here, if you exit from Piety or
    interrupt it, you will also exit from Python.

- **run_piety_writers**: similar to *run_piety*, but also starts with two
    writer tasks defined.  Invoked by the *piety_writers* command.


Revised Oct 2013
