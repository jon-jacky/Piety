
scripts
=======

This directory contains Python scripts that run applications as tasks
or jobs under the Piety scheduler.  See docstrings (comment headers)
and inline comments in each module for directions and explanations:

- **embedded**: Runs the Piety scheduler with two concurrent file writer
   tasks, but without an interactive interpreter.  Shows that Piety
   can run in a "headless" mode with no console, as is needed in some
   embedded systems.

- **piety**: Runs the Piety scheduler on a single console session
    (task) with three jobs: the *pysh* shell, the *ed* line
    editor, and the *edd* display editor.  Also creates (but does 
    not start) two file writer tasks.  Demonstrates different
    techniques for naming, invoking, exiting, editing jobs and tasks.
    
- **piety.no_defaults**: Similar to  *piety* script, except it uses different
   syntax to define jobs, with no default arguments.  Does not create
   file writer tasks (but they are easy to create "by hand" in the pysh shell).

- **session**: Similar to *piety* script, except it runs just the console
    session and its three jobs without the Piety scheduler.  

Revised February 2015
