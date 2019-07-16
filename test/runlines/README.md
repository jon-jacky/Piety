runlines
========

Tests for commands that execute Python code from text buffers.
The commands execute the code at top level (in the *main* module),
they do not import the buffer as a module.
The test cases are just files of Python code you can load into buffers.
Pertinent commands:

- *B filename*: Load file named *filename* into a new buffer with that name.

- *R bufname*: Execute the entire buffer named *bufname*.
Default is the current buffer.

- *linesP*: Execute selected lines in the current buffer in
command mode.  *lines* is a single line or range of lines indentified by
one or two *ed* line addresses.  Default is *dot*, the current line.

- *^T*: Execute the current selection from *mark* (inclusive) to
*dot* (exclusive) in display mode.   Default if there is no *mark* is *dot*.

Some of the test files.  Several are designed to check handling of newlines 
and empty lines in code.  We suspect this might be an issue.  See
the comment in the standard library module *codeop.py*, that begins
'Compile three times: ...'

- *empty.py*: empty file

- *empty1.py*: file containing only one newline

- *empty2.py*: file containing only two newlines

- *comment1.py*: file containing one comment line followed by one newline

- *dtimport.py*: two lines of code: *import datetime* then
*datetime.datetime.now()* with no trailing newline

- *dtimport1.py*: contents of *dtimport.py* then one trailing newline
(this is the typical form)

- *dtimport2.py*: contents of *dtimport.py* then two trailing newlines

- *dtimport_blank1.py*: A blank line (just a newline) followed by contents of
*dtimport.py*

- *dtimport_blank2.py*: *dtimport.py* contents, but with a blank line between
the first and second lines of code

Revised July 2019

