
scripts
=======

This directory contains Python scripts that run applications as tasks
or jobs under the Piety scheduler.  See docstrings (comment headers)
and inline comments in each module for directions and explanations:

- **console_tasks.py**: Creates console jobs and session used by the
    *piety* and *session* scripts.  Demonstrates different techniques
    for creating, naming, and exiting jobs and tasks.

- **embedded**: Runs the Piety scheduler with two concurrent file writer
   tasks, but without an interactive interpreter.  Shows that Piety
   can run in a "headless" mode with no console, as is needed in some
   embedded systems.

- **piety**: Runs the Piety scheduler on a single console session
    (task) with three jobs: the *pysh* shell, the *ed* line editor,
    and the *edd* display editor.  Also creates and runs two file
    writer tasks.  The jobs and tasks are created in *console_tasks*
    and *writer_tasks*.

- **piety.no_defaults**: Similar to  *piety* script, except it uses different
   syntax to define jobs, with no default arguments.  Does not create
   file writer tasks (but they are easy to create "by hand" in the pysh shell).

- **session**: Similar to *piety* script, except it runs just the
    console session and its three jobs without the Piety scheduler and
    without the writer tasks.  The jobs are created in
    *console_tasks*.

- **writer_tasks.py**: Creates writer tasks used by the *embedded* and
    *piety* scripts.

Revised April 2015
