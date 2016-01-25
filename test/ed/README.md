
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

The *.ed* files also test command mode.  They contain sequences of
*ed* commands, the same commands as in the corresponding *.sh* files,
but without the *q* (quit) command.  To execute the test in an *.ed*
file, load it into *ed* buffer using an *e*, *r*, or *B* command, then
run the test by calling the *do_cmds* API call on the buffer contents.

The *.log* files are output from *python test_ed.py > test_ed.log*,
*./test_ed.sh > test_ed.sh.log* etc.  The contents of the *.log* file
in this repository should be the same as the output you get when you
run that test script on your recent version of *ed.py*.

The *.sh* files whose basenames end in *3* (for example *sample3.sh*)
use the *python3* command instead of *python* to run Python version 
3 on systems where the *python* command runs Python version 2.

The *.txt* files here are samples used to demonstrate text editing.
The *ed.py.txt*, *ed.md.txt*, and *README.md.txt* here are not
up-to-date with their original namesakes.

The *.txt.save* files are files written by *ed* when executing tests
with the corresponding names.   The contents of the *.txt.save* file
in this repository should be the same as the *.txt* file you get when you
run that test script on your recent version of *ed.py*.

Revised January 2016
