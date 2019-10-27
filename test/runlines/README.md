runlines
========

Tests for commands that execute Python code from text buffers.
The commands execute the code at top level (in the *main* module),
they do not import the buffer as a module.
The test cases are just files of Python code you can load into buffers.
Pertinent commands:

- *B filename*: Load file named *filename* into a new buffer with that name.

- *linesP*: Execute selected lines using the *push* method from Python *code*
module *InteractiveConsole* class. Here *lines* is a single line or range of
lines indentified by one or two *ed* line addresses. Default is *dot*, the
current line.

- *linesR*: Execute selected lines using the builtin *exec* function.

- *^T*: In display mode, execute the current selection using *push*
The *selection* is the lines from *mark* (inclusive) to
*dot* (exclusive). The default selection is *dot* if there is no *mark*.

We provide both *P* and *R* commands because the behavior of *push* and *exec*
are different. *P* treats the lines of code the same as the interactive Python
interpreter.  It prints the values of expressions even without any explicit
*print* calls, but it requires that the code be formatted with a blank line
preceding every *outdent* (a line with less indentation than its predecessor).

For example,
both *defs_noblank.py* and *if_block_noblank.py* in this directory
are correct Python code;
each runs without errors when it is *import*ed.
Each of these modules has an *outdent* with no preceding blank line.
When the contents of these modules are executed by the
*P* or *^T* commands, *edsel* reports a synax error at the outdented
statement.  The modules *defs.py* and *if_block.py* are the same, except there
is a blank line between the indented block antd the following outdented
statement.   *P* and *^T* run these modules without errors.

This same quirk exhibited by the standard interactive Python interpreter.
This is what happens if you type the lines in *if_block.py* at the interpreter:

    >>> if True:
    ...     1 + 1
    ...
    2
    >>> print('It worked')
    It worked

This is what happens if you type the lines in *if_block_noblank*:

    >>> if True:
    ...     1 + 1
    ... print('It worked')
      File "<stdin>", line 3
        print('It worked')
        ^
    SyntaxError: invalid syntax

Since the behavior of *P* and *^T* in this situation is the same
as the stardard interactive Python interpreter, we do not consider this
behavior to be a bug.  Instead, we also provide an *R* command that
uses builtin *exec* which runs the code instead of reporting an error.

We discovered this behavior when we got a syntax error running
*redirect_noblank.py* with the *P* command. We found we could work around the
problem by adding a blank line before the outdent in *redirect.py*.

Some of the test files.  Several are designed to check handling of newlines
and empty lines in code.  We suspected this might be an issue.  See
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

Revised Oct 2019

