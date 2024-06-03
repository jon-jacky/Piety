
tasking
=======

Modules that support tasking experiments with threads or coroutines
and our editors.

The editors are not just for creating text. Python commands including
concurrent tasks can use the *writer* module here to redirect their output to
editor buffers and windows, so the editors can be used for data capture and
animated display.
  
We need  our custom *pysh* Python interpreter, defined in the *pyshell*
module here, for these tasking experiments.  It enables us to restore the
cursor to the correct location in the Python command line after a background
task updates an editor display window. This is not possible with the
standard Python interpreter.

The *pysh* command prompt is >> with just two darts, to distinguish it from
the standard Python prompt >>> with three darts.
 
### Files ###

- **pyshell.py**: Defines custom Python interpreter *pysh* that 
  enables us    to restore the cursor to the correct location in the
  Python command line    after a background task updates an editor
  display window.

- **writer.py**: Functions that put text into our editor buffers and windows,
  intended to be called from background tasks.  Code here also restores
  the cursor to the correct location in the *pysh* Python
  command line,   or in a display editing window, after a background task
  updates another window.

- **writer.txt**:  Notes on *writer.py*.
 
Revised Jun 2024

