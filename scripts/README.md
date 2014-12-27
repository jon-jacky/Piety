
Piety scripts directory
=======================

Run applications using the Piety modules.

To conveniently use these scripts, this directory should be on your
execution *PATH*.  Or, its contents should be installed in some
directory that is on your execution *PATH*.  See *bin/piety_paths*.

These scripts are platform independent except for the initial hashbang
line, which are only effective on a Unix-like host.  On a Unix-like
host, you can run a script by simply naming it on the command line:
*piety* etc.  On other systems, you should be able to run them with the
Python interpreter: *python piety* etc.

These scripts use the *console* module to run command line
applications, but do not use the Piety scheduler.

- **pyshc**: Runs the *pysh* Python shell.

- **edc**: Runs the *ed* line editor.

- **eddc**: Runs the *edd* display editor.

These scripts define Piety tasks, then start the Piety scheduler:

- **pysh**: Start a Piety session running the *pysh* Python shell.
 You can then use this shell to create and run more tasks.

- **writers**: Similar to the *pysh* script, but also creates
    two concurrent file writer tasks, which you can start and stop
    from the shell.

- **embedded**: Starts a Piety session running two concurrent file writer
   tasks, but without an interactive interpreter.  Shows that Piety
   can run in a "headless" mode with no console, as is needed in some
   embedded systems.

- **edd**: Starts Piety with the *pysh* shell, *ed* line editor, and
    *edd* display editor tasks.  Exhibits a coding style including
    naming conventions for task, console, and key instances.  Demonstrates
    how *ed* and *edd* provide two different user interfaces to the
    same editor state, so you can switch back and forth and keep the
    same buffers, cursor position, etc.

Revised December 2014
