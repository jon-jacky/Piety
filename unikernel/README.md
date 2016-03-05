
unikernel
=========

A *unikernel* comprises an application together with a minimal
operating system configured to support just that application.  

These files were part of an experiment in November 2015 to build a
unikernel for running Piety, based on the NetBSD [Rumprun
unikernel](https://github.com/rumpkernel/rumprun).

I learned that the current version of the Rumprun unikernel does not
support keyboard input, so it cannot run the Piety user interface (the
shell and the editors).  So I set aside this experiment for now.

The problem is discussed in this
[issue](https://github.com/rumpkernel/rumprun/issues/64).  The issue
remains open at the time of this writing (March 2016) and may be fixed
in the future.

Revised March 2016
