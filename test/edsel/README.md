
edsel tests
===========

Tests for *edsel.py*.  The directions and explanations in
*test/ed/README.md* also apply here.  Comments in each file explain
its test.

The *edsel.py* display editor imports the *ed.py* line editor and
supports all of its commands and API calls.  However, the *.py* and
*.sh* test scripts for *ed* in *test/ed/* do not work with *edsel*; it
is necessary to make slighty revised versions that import or invoke
*edsel* instead of *ed*.  The *sample.py* and *sample3.sh* scripts in
this directory are examples.   

All of the *.ed* scripts in *test/ed/* work with *edsel* without any
changes, because they do not mention the *ed* module name.

The *.edsel* scripts here in *test/edsel/* are files of *ed* and
*edsel* commands that test *edsel* features that are not present in
*ed*: display functions and window management commands.  

When you execute an *.ed* or *.edsel* script, you can see the window contents
update as the test runs.  Each command echoes in the scrolling command
region, followed by a short delay so you can observe its effect.  The
echo and delay can be adjusted or suppressed by two optional *x*
parameters that follow the buffer name: echo (boolean) and delay
(float), which default to *True* and *0.2* seconds.  So *x sample.ed 0
0* suppresses both echo and delay.

The names of some scripts are made from the sequence of commands
they contain, for example *lio2o1xn.edsel*.


Revised March 2016
