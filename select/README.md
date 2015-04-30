
select
======

This directory contains an *eventloop* module with a *run* method.

This is a platform-dependent module because it uses Unix *select*.

The platform-independent *piety* module imports the *eventloop* module
from this directory to run Piety on Unix-like hosts (including Linux
and Mac OS X).

Revised April 2015
