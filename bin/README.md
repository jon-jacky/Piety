
Piety bin directory
=====================

This directory contains scripts for running Piety on a Unix-like host
operating system, including Linux and Mac OS X. 

Most of these are *startup scripts* that define Piety tasks, then
start the Piety scheduler.  These scripts are platform independent
except for the initial hashbang line (which are only effective on a
Unix-like host).

To conveniently use Piety, this directory should be on your execution
*PATH*.  Or, its contents should be installed in some directory that
is on your execution *PATH*.  See *piety_paths* in this directory:

- **piety_paths**: assigns paths for running Piety.  To prepare to
 use Piety, execute this script, or put the commands from this script
 into your *.profile* or *.bashrc*.  These commands add *Piety/bin* to
 the execution *PATH*, and adds *Piety/piety* and *Piety/samples* to
 the *PYTHONPATH*.

Startup scripts:

- **piety**: Start a Piety session running an interactive Python
 interpreter, using the *pysht* shell.  You can then use this shell to
 create and run more tasks.

- **writers**: Similar to the *piety* script, but also starts with
    two concurrent file writer tasks, which you can start and stop
    from the shell.

- **ed**: Start Piety with the *pysht* shell and *ed* line editor
    tasks.  This script demonstrates a method to ensure that console
    focus is switched between the two console tasks.  However, the
    method it uses works, but is now deprecated.

- **edd**: Start Piety with the *pysht* shell, *ed* line editor, and
    *edd* display editor tasks.  This script demonstrates how to
    *ensure that console focus is switched between the three console
    *tasks, using the current, recommended method involving
    **console.Command*.

Revised October 2014
