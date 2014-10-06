
Piety bin directory
=====================

This directory contains scripts for running Piety on a Unix-like host
operating system, including Linux and Mac OS X.

To conveniently use Piety, this directory should be on your execution
*PATH*.  Or, its contents should be installed in some directory that
is on your execution *PATH*.  See *piety_paths* in this directory.

Some of the scripts are:
  
- **piety_paths**: assigns paths for running Piety.  .  To prepare to
 use Piety, execute this script, or put the commands from this script
 into your *.profile* or *.bashrc*.  These commands add *Piety/bin* to
 the execution *PATH*, and adds *Piety/piety* and *Piety/samples* to
 the *PYTHONPATH*.

- **piety**: Start a Piety session running an interactive Python
 interpreter, using the pysht shell.  You can then use this shell to create
 and run more tasks.

- **writers**: Similar to the *piety* command, but also starts with
    two concurrent file writer tasks.

- **ed**: Start Piety with Python shell and ed line editor tasks.
     At startup, the shell has the console focus.

- **edd**: Similar to **ed**, but provides the *edd* display editor.

Revised October 2014
