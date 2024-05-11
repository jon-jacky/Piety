
Modular structure
=================

The Piety directories and modules are designed to enable Piety to run on
different platforms and in different configurations.

A *platform* is a host operating system or a bare machine (including
virtual machines), including the Python interpreter itself (CPython,
PyPy, Micro Python, ...).  A *configuration* is a collection of
available devices, possibly including a console terminal, but also
allowing for "headless" configurations with no console (as are
sometimes used for embedded systems).

It is possible to customize Piety systems by choosing different
subsets and combinations of modules.  To adapt to different
platforms and configurations, you can create modules with the
same name and same API (but different internals) stored in
different directories.  

For example, we have the directory *unix* containing the module
*terminal.py*.  To support a different platform,  we might add a directory
*windows* that also contains a module *terminal.py* with  the same
function names and arguments but different function bodies.

The *unix* and *windows* directories and their contents are platform dependent.
But modules that import the *terminal* module and call its functions
are platform independent.  Plaatform dependent and platform independent
modules must be kept in different directores so Piety can be configured
for different platforms by defining different *PYTONPATH*

For each platform, the platform dependent modules are included by adding
their platform dependent directories to the *PYTHONPATH* and excluding the
alternate platform dependent directories.  To help with this, there are
commands in the *bin* directory.

Different configurations (that support different collections of hardware etc.)
can be supported in the same way as different platforms.
 
Revised May 2024


