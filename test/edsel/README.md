
edsel tests
===========

Tests for *edsel.py*.  The directions and explanations in
*test/ed/README.md* also apply here.

The *edsel.py* display editor imports the *ed.py* line editor and
supports all of its commands and API calls.  However, the *.py* and
*.sh* test scripts for *ed* in *test/ed/* do not work with *edsel*; it
is necessary to make slighty revised versions that import or invoke
*edsel* instead of *ed*.  The *sample.py* and *sample3.sh* scripts in
this directory are examples.

All of the *.ed* scripts for *ed* in *test/ed/* do work with *edsel*,
because they do not mention the *ed* module name.  They are just files
of *ed* commands that are loaded into an editor buffer (in *ed* or
*edsel*) and executed with the *x* command.

The *.ed* scripts that test functionality that is present in both
editors are kept in *test/ed/*.  The *.ed* scripts here in
*test/edsel/* only test *edsel* features that are not present in
*ed*: display functions and window management commands.

When you execute an *.ed* script, you can see the window contents
update as the test runs.  Each command echoes in the scrolling command
region, followed by a short delay so you can observe its effect.  The
echo and delay can be adjusted or suppressed by two optional *x*
parameters that follow the buffer name: echo (boolean) and delay
(float), which default to *True* and *0.2* seconds.  So *x sample.ed 0
0* suppresses both echo and delay.

Revised February 2016
