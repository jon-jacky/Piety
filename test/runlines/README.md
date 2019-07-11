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

Some of the files:

- *empty.py*: empty file

- *empty1.py*: file containing only one newline

- *empty2.py*: file containing only two newlines

- *comment1.py*: file containing one comment line followed by one newline

- *dtimport.py*: two lines of code: *import datetime* then
*datetime.datetime.now()* with no trailing newline

- *dtimport1.py*: two lines: *import datetime* then *datetime.datetime.now()*
with one trailing newline (this is typical form).

- *dtimport2.py*: two lines: *import datetime* then *datetime.datetime.now()*
with two trailing newlines

- *dtimport_blank1.py*: A blank line (just a newline) followed by *dtimport.py*
contents

- *dtimport_blank2.py*: *dtimport.py* contents, but with a blank line between
the first and second lines of code

Revised July 2019

