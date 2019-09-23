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

- *exprs.py*: several expressions and assignment statements, with no blank
lines

- *exprs_blank1234.py*: same as *exprs.py*, but with one or more blank lines
separating groups of statements

- *exprs_errs.py*: similar to *exprs.py*, but some statements contain undefined
variable or syntax errors

- *defs.py*: define two functions, separated by a blank line

- *defs_noblank.py*: like *defs.py*, but no blank line between the definitions

- *defs_errs.py*: like *defs.py*, but each definition is preceded by a similar
definition containing a syntax error

- *if_block.py*: an *if* statement with an indented body followed by a blank
line, then a *print* statement

- *if_block_noblank.py*: like *if_block.py*, but no blank line between the
indented *if* body and the *print* statement

Both *defs_noblank.py* and *if_block_noblank.py* are correct Python code;
each runs without errors when it is *import*ed.
Each of these modules has an *outdent* where an indented block of code is
followed by an unindented statement, with no blank line between.  When
the contents of these modules are executed by *edsel* using the
*R*, *P*, or *^T* commands, *edsel* reports a synax error at the outdented
statement.  The modules *defs.py* and *if_block.py* are the same, except there
is a blank line between the indented block antd the following outdented
statement.   The *R*, *P*, or *^T* commands run these modules without errors.

This same quirk exhibited by the standard interactive Python interpreter.
This is what happens if you type the lines in *if_block.py* at the interpreter:

    >>> if True:
    ...     1 + 1
    ...
    2
    >>> print('It worked')
    It worked

This is what happens if you tupe the lines in *if_block_noblank*:

    >>> if True:
    ...     1 + 1
    ... print('It worked')
      File "<stdin>", line 3
        print('It worked')
        ^
    SyntaxError: invalid syntax

Since the behavior of *edsel* *R* *P* and *^T* in this situation is the same
as the stardard interactive Python interpreter, we do not consider this
behavior to be a bug and we will not attempt to fix it.

Revised Sep 2019

