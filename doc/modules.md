
Modular structure
=================

The Piety [directories](directories.md) and modules are designed to
enable Piety to run on different platforms and in different
configurations.  

A *platform* is a host operating system or a bare machine (including
virtual machines), including the Python interpreter itself (CPython,
PyPy, Micro Python, ...).  A *configuration* is a collection of
available devices, possibly including a console terminal, but also
allowing for "headless" configurations with no console (as are
sometimes used for embedded systems).

It is possible to customize Piety systems by choosing different
subsets and combinations of modules.  To adapt to different
platforms and configurations, there are some modules with the
same name and same API (but different internals) stored in
different directories: for example, we have *select/eventloop.py* and
*asyncio/eventloop.py*.  The chosen module can be included by
adding its directory to the *$PYTHONPATH* and excluding the other.
To help with this, there are commands in the *bin* directory.

In the following discussion, *use* or *depend on* means *import*.  The
design attempts to minimize dependencies among modules.

- Modules that depend on particular platforms (host operating systems)
  or configurations (devices) are separated out in directories with
  specific names that indicate the dependence, for example *unix* or
  *select* or *vt_terminal*.  Functionally-equivalent modules within
  these directories provide the same API.  In particular, these
  modules have the same generic names: *terminal*, *eventloop*,
  *keyboard*, *display*.  The functions (etc.) within these modules
  also have the same generic names: *run*, *self_insert_char*,
  *kill_line* etc.  The bodies of those functions can contain
  platform- and device-specific code.  Modules that use (import) any
  of these are not platform- or device-dependent because they import
  modules and call functions by their generic names.  The chosen
  versions are selected by placing their directories on the
  *$PYTHONPATH*.

- Modules that are not platform- or device-dependent are written
  in *pure Python*: They do not use C extensions, or modules that
  wrap libraries written in other languages.  Those can limit the
  platform to one particular Python interpreter (usually CPython).
  A requirement for a particular Python interpreter is an example of
  a platform dependence.

- The *piety* module in the *piety* directory is the core of the Piety
  operating system.  It does not depend on any particular devices (in
  particular, it does not require a console).  It is
  platform-independent, but it must import a platform-dependent
  *eventloop* module from a directory that contains one (currently,
  from the *select* or *asyncio* directory).  

- The *piety* module and all the *eventloop* modules import
  *schedule*.  The platform-independent *schedule* module avoids
  duplicating code in the *eventloop* modules and separates
  platform-independent code from the platform-dependent code in the
  *eventloop* modules.

- The modules in the *console* directory are used by terminal
  applications.  They are platform- and device- independent.  They
  access all terminal functions by importing 
  modules from device-dependent directories such as *unix* and
  *vt_terminal*.

- The modules in the directories *applications*, *editors*, and
  *shell* are applications (the Python shell is just another
  application).  An application does not depend on any modules in
  *piety*; in fact, it must be able to run without the Piety event loop.
  To demonstrate this, every application can be run from the host's
  *python* command or in any Python interpreter session (by invoking the
  application's *main* function, for example).  Applications are also
  platform- and device- independent, by observing the same discipline as
  modules in *console*.  Applications are included in the Piety
  repository just as a convenience, and any application may be removed
  or separated out to a different repository in the future.

- None of the Piety operating system modules in *piety*, *console*, or
  anywhere else depend on any application modules.
  
- The modules in the *scripts* directory run applications as tasks or
  jobs under Piety.  These scripts typically use modules
  from the *piety*, *console*, and application directories.  They
  can use any modules.  Avoiding platform- or
  device-specific code in scripts makes it possible for them to be re-used
  on different systems.

- None of the Piety operating system modules or applications depend on any
  contents of the *scripts* directory

Revised May 2015
