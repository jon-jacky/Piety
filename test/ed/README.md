Editor tests
============

Tests for *ed.py*.  For explanations and instructions, see each
module's docstrings.

The *.py* files test the API.  The *.sh* files test command mode.

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
