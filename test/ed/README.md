
ed tests
========

Tests for *ed.py*.  For explanations and instructions, see each
module's docstrings.

The *.py* files test the API.  They contain sequences of API calls.
To execute these tests, run them as Python programs.

The *.sh* files test command mode.  They contain sequences of *ed*
commands, along with shell commands to start *ed* and read the *ed*
commands from the file.  To execute these tests, run them as shell
scripts.

The *.sh* files whose basenames end in *3* (for example *sample3.sh*)
use the *python3* command instead of *python* to run Python version 
3 on systems where the *python* command runs Python version 2.

The *.ed* files also test command mode.  They contain sequences of
*ed* commands.  Each *.ed* file contains the same *ed* commands as in
the corresponding *.sh* files, but without any shell commands and
without the *ed* *q* (quit) command.  

The *.edo* files are like *.ed* files except, in addition to *ed*
commands, they also contain Python commands prefixed with *!*.  The
*ed* program cannot process tjhese commands; it is necessary to use
*edo*.

We use *.ed* and *.edo* scripts in two ways: interactively and
non-interactively.

It is helpful to execute *.ed* test scripts interactively at first to
observe the behavior and confirm that the editor performs as intended.
To do this, you must run *edo* not *ed*, because *edo* provides
the *x* script execution command.  Load the script into an
editor buffer using an *e*, *r*, or *B* command: *B sample.ed*, for
example.  Then change back to the *main* buffer with *b main* and
execute the test in that buffer with the *x* command: *x sample.ed*.
Each command echoes as it executes, then there is a short delay before
the next command so you can see its effect. The echo and delay can be
adjusted or suppressed by two optional *x* parameters that follow the
buffer name: *x sample.ed 0 0* suppresses both echo and delay.  For example:

    ... $ python3 -i -m edo
    :B sample.ed
    sample.ed, 18 lines
    :b main
    .   main                 0  None
    :x sample.ed 1 2
    ...
    ... sample.ed executes, echoes commands, waits 2 sec after each command
    ...
    :q
    >>> ^D
    ... $

After the script finishes, type *q* at the prompt to exit the editor,
then exit from Python.

We execute *.ed* scripts non-interactively to save editor output for
regression testing.  For this we do not need the *x* command so we can
run *ed* not *edo*.  We use redirection at the command line
to feed the commands to the editor and collect the output:

    ... $ python3 -m ed < sample.ed > sample.ed.log
    ...
    File "/Users/jon/Piety/editors/ed.py", line 490, in main
       line = input(prompt())
    EOFError: EOF when reading a line

The *EOFError* here does not indicate a problem, it appears because
there is no *q* command in the *.ed* script.  Now the *.log* file
contains the editor output.  It can be saved as a reference standard,
or compared to an earlier reference to check whether behavior has changed.

The *.log* files are output from *python test_ed.py > test_ed.log*,
*./test_ed.sh > test_ed.sh.log* etc.  The contents of the *.log* file
in this repository should be the same as the output you get when you
run that test script on your recent version of *ed.py*.

The *.txt* files here are samples used to demonstrate text editing.
The *ed.py.txt*, *ed.md.txt*, and *README.md.txt* here are not
up-to-date with their original namesakes.

The *.txt.save* files are files written by *ed* when executing tests
with the corresponding names.   The contents of the *.txt.save* file
in this repository should be the same as the *.txt* file you get when you
run that test script on your recent version of *ed.py*.

The command scripts *check_ed.sh* and *check_ed_txt.sh* automate
running *.ed* or *.edo* scripts non-interactively and using the *diff*
command to compare the resulting *.log* and *.txt* files against reference
versions.  These two scripts are used by *check_many.sh* to run all
the *.ed* and *.edo* scripts.

Revised Jan 2018

