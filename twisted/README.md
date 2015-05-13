
twisted
=======

This directory contains an *eventloop* module with a *run* method.

This is a platform-dependent module because it requires *Twisted*.

The platform-independent *piety* module imports the *eventloop* module
from this directory to run Piety on hosts where *Twisted* is installed.

Revised May 2015
