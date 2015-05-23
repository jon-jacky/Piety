
twisted
=======

This directory contains an *eventloop* module that uses the Twisted event loop
instead of the usual Piety event loop based on Unix *select*.

This is a platform-dependent module because it requires *Twisted*.

The platform-independent *piety* module imports the *eventloop* module
from this directory to run Piety applications, tasks, and jobs with the 
Twisted event loop instead of the usual Piety event loop.

To import *twisted/eventloop* instead of the usual *select/eventloop*.
put the *twisted* directory on your *PYTHONPATH* instead of the
*select* directory.  A convenient way to achieve this is to run tje
*bin/twisted_paths* command instead of the usual *bin/paths*.

Revised May 2015
