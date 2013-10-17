
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

- **piety**: Run a Piety session.  Start Python, import the essential
  Piety modules, and start a single console task running a Python 
  interpreter.

The programs are:

- **run_piety**, start Piety with Python shell running.  Invoked by
    the *piety* command.

- **run_piety_writers**, start Piety with Python shell running and two
    writer tasks defined, but only one running.


Revised Oct 2013
