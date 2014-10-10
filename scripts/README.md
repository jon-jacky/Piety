
Piety scripts directory
=======================

Most of these are *startup scripts* that define Piety tasks, then
start the Piety scheduler.  

To conveniently use these scripts, this directory should be on your
execution *PATH*.  Or, its contents should be installed in some
directory that is on your execution *PATH*.  See *bin/piety_paths*.

These scripts are platform independent except for the initial hashbang
line, which are only effective on a Unix-like host.  On a Unix-like
host, you can run a script by simply naming it on the command line:
*piety* etc.  On other systems, you should be able to run them with the
Python interpreter: *python piety* etc.

Startup scripts:

- **piety**: Start a Piety session running an interactive Python
 interpreter, using the *pysht* shell.  You can then use this shell to
 create and run more tasks.

- **writers**: Similar to the *piety* script, but also starts with
    two concurrent file writer tasks, which you can start and stop
    from the shell.

- *embedded*: Starts a Piety session running two concurrent file writer
   tasks, but without an interactive interpreter.  Shows that Piety
   can run in a "headless" mode with no console, as is needed in some
   embedded systems.

- **ed**: Start Piety with the *pysht* shell and *ed* line editor
    tasks.  *Warning*: this script demonstrates a to get console
    focus to switch between the two console tasks.  However, the
    method it uses works, but is now deprecated.

- **edd**: Start Piety with the *pysht* shell, *ed* line editor, and
    *edd* display editor tasks.  This script demonstrates recommended
    coding style.  For example, it shows how to ensure that console focus is
    switched among the console tasks by using *console.Command*.

Revised October 2014
