runlines
========

Tests for commands that execute Python code from text buffers.
The test cases are just files of Python code you can load into buffers.

- *B filename*: Load file named *filename* into a new buffer with that name.

- *R bufname*: Execute the entire buffer named *bufname*.
Default is the current buffer.

- *linesP*: Execute selected lines in the current buffer in
command mode.  *lines* is a single line or range of lines indentified by
one or two *ed* line addresses.  Default is *dot*, the current line.

- *^T*: Execute the current selection from *mark* (inclusive) to
*dot* (exclusive) in display mode.   Default if there is no *mark* is *dot*.

Revised July 2019

