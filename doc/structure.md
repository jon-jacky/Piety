
Modular structure and design rules
==================================

The Piety [directories](../directories.md) and modules are designed to
enable Piety to run on different platforms and in different
configurations.  A *platform* is a host operating system or a bare
machine (including virtual machines), including the Python interpreter
itself (CPython, PyPy, Micro Python, ...).  A *configuration* is
a collection of available devices, possibly including a console
terminal, but also allowing for "headless" configurations with no
console (as are sometimes used for embedded systems).

In the following discussion, *use* or *depend on* means *import*.
The design minimizes dependencies among modules.

We observe these design rules:

- Modules that depend on particular platforms (host operating systems)
  or configurations (devices) are to be avoided, except where
  necessary.  They must be separated out in directories with specific
  names that indicate the dependence, for example *unix* or
  *vt_terminal*.  The modules within these directories must have
  generic names, for example *terminal*, *keyboard*, *display*.  The
  functions (etc.)  within these modules must also have generic names:
  *self_insert_char*, *kill_line* etc.  The bodies of those functions
  can contain platform- and device-specific code.  Modules that depend
  on different platforms and devices go into different directories
  with other specific names: for example *printing_terminal* or
  *framebuffer_terminal* etc.  But the
  modules in these directories must also have the same generic module
  names and function names.  Modules that use any of these are not
  platform- or device-dependent because they import modules and call
  functions by their generic names.  Then Piety can be configured for
  different platforms and devices by including or omitting different
  subsets of the specialized directories from *PYTHONPATH*.  This can
  be accomplished by providing appropriate scripts in the *bin*
  directory.

- Modules that are not platform- or device-dependent must be written
  in *pure Python*: They must not use C extensions, or modules that
  wrap libraries written in other languages.  Those can limit the
  platform to one particular Python interpreter (usually CPython).

- The modules in *scheduler* directory are the core of the Piety
  operating system.  They must not depend on any specific platform,
  device, or application, so they must not depend on modules in
  *unix*, *vt_terminal*, *console* or in any application directories.
  (At this writing the *piety* module violates this rule; it depends
  on the Unix *select* function.  We will fix this.)

- The modules in the *console* directory are used by terminal
  applications.  They must be platform- and device- independent.  They
  must access all terminal functions by importing generically-named
  modules from device-dependent directories such as *unix* and
  *vt_terminal*.

- The modules in the directories *applications*, *editors*, and *shell*
  are applications (the Python shell is just another application).  An
  application must not depend on any modules in *scheduler*; in fact,
  it must be able to run without the Piety scheduler.  To demonstrate
  this, every application must have a *main* method that can be run
  from the host's *python* command or in any Python interpreter
  session.  Applications must also be
  platform- and device- independent, by observing the same discipline
  as modules in *console*.  Applications are included in the Piety
  repository just as a convenience, and any application may be removed
  or separated out to a different repository in the future.

- The modules in the *scripts* directory run applications as tasks or
  jobs under the Piety sheduler.  These modules typically use modules
  from the *scheduler*, *console*, and application directories.  They
  can use any modules, but it is good practice to avoid platform- or
  device-specific code.

Revised February 2015
