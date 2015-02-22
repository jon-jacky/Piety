
scripts
=======

This directory contains Python scripts that run applications as tasks
or jobs under the Piety scheduler:

- **embedded**: Runs the Piety scheduler with two concurrent file writer
   tasks, but without an interactive interpreter.  Shows that Piety
   can run in a "headless" mode with no console, as is needed in some
   embedded systems.

- **piety**: Runs the Piety scheduler on a single console session
    (task) with three jobs: the *pysh* shell, the *ed* line
    editor, and the *edd* display editor.  The docstring (comment header)
    in this script explains how to create and run concurrent file 
    file writer tasks from the shell.

- **piety.no_defaults**: Like the *piety* script, except it uses different
   syntax to define jobs, with no default arguments.

- **session**: Like the *piety* script, except it runs just the console
    session and its three jobs without the Piety scheduler.  

Revised February 2015
