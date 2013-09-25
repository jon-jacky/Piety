piety
=====

The **piety** directory contains the Piety operating system code: the
scheduler, console, shell, and some utilities.

Piety runs in a single Python interpeter session.  All Piety software,
including both operating system and applications, executes in this
session.  The session might run on a host operating system or on a
bare machine (with the minimum of hardware support in C or assembler).
There are only a few platform-dependent modules.  Most modules
developed for Piety on a host operating system should also work on a
bare machine.

### Scheduler ###

The *piety* module schedules multiple tasks in a single Python
interpreter session.  To run the Piety operating system: start Python,
import the *piety* module, create some *piety.Task* instances, then
call *piety.run*.  Usually, one of the tasks is a Python shell, so you
can continue to interact while Piety is running.  See the examples in
the *samples* directory.  More details appear in docstrings.

Piety is event-driven.  Each Piety task is defined by an *event*, a
*handler*, a *guard*, and a *name*.  A handler can be any Python
callable, including a function, method, generator, or coroutine.  A
guard can be any callable that returns a Boolean.  The scheduler is an
event loop that may invoke a task's handler when its event occurs and
its guard is true.  Then the handler runs until it returns control to
the scheduler.  There is no preemption.  This is called *cooperative
multitasking*.

It is the programmer's obligation to ensure that each handler finishes
quickly enough for acceptable performance.  Many existing Python
applications and modules are not designed to cooperate in this way ---
instead they take over the Python session, postponing all other tasks.
However, it may be possible to adapt some of them.

### Console ###

The *console* module contains a skeleton command line application.
It defines a class *Console*, with a *getchar* method that gets a single
character typed at the console keyboard, and adds it to a command line
(usually).  When *getchar* gets a line terminator character, it calls a
command function and passes the command line to it.  *Getchar* also
handles some editing functions and other control keys.

The *getchar* method (including the command function it may call) can
be one of the handlers scheduled by *piety.run*.  Other Piety tasks
can run while the user is entering or editing the command line.

The command function is passed as an argument to the *Console*
constructor, so this same class can act as the front end to any
command line application.  The command function can invoke the Python
interpreter itself, so a *Console* instance can act as Piety's Python
shell.

### Shell ###

The *pysht* module defines a function *mk_shell* that accepts
configuration settings and returns a command function that can be
passed to the *Console* constructor, to make that *Console* instance
into a Python shell.

### Terminal ###

To use *getchar*, the console must be put into single-character mode,
by calling the *setup* function in the *terminal* module.  The
*restore* function returns to the previous mode.

### Modules ###

These are the modules in the *piety* directory.  For more details see
their docstrings.

- **piety**, scheduler, defines *Task* class and *run* function

- **console**, skeleton command line application

- **pysht**, Python shell, configures *console* to provide
    a Python interpreter.

- **terminal**, utilities used by *console*

