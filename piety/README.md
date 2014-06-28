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

Piety is event-driven.  Each Piety task identifies an *event*, a
*handler*, and an *enabling condition*.  A handler can be any Python
callable, including a function, method, generator, or coroutine.  An
enabling condition can be any callable that returns a Boolean.  The
scheduler is an event loop that may call a task's handler when its
event occurs and its enabling condition is true.  Then the handler
runs until it returns control to the scheduler.  There is no
preemption.  This is called *cooperative multitasking*.

All software that runs in Piety must be organized as a collection of
functions or methods (etc.) that can be called as handlers.  It is the
programmer's obligation to ensure that each handler finishes quickly
enough for acceptable performance.  Many existing Python applications
and modules are not designed to cooperate in this way --- instead they
take over the Python session, postponing all other tasks.  However, it
may be possible to adapt some of them.

### Console ###

The *console* module contains a skeleton command line application.
It defines a class *Console*, with a *getchar* method that gets a single
character typed at the console keyboard, and adds it to a command line
(usually).  When *getchar* gets a line terminator character, it calls a
command function and passes the command line to it.  *Getchar* also
handles some editing functions and other control keys.

The *getchar* method (including the command function it may call) can
be one of the handlers scheduled by *piety.run*, called each time the
user types a single key.  Other Piety tasks can run while the user is
entering or editing the command line.

The command function is passed as an argument to the *Console*
constructor, so this same class can act as the front end to any
command line application.  The command function can invoke the Python
interpreter itself, so a *Console* instance can act as Piety's Python
shell.

It is possible to have more than one console task in a Piety session.
For example, it is typical to have a Python shell and an editor.  In
that case it is necessary to ensure that, at any time, only one
console task has the *focus*.  Console keyboard input only goes to the
task with the focus; its command function is called when the command
line is complete.  This task is identified by assigning that task to
the *focus* variable in the *console* module.  Each console task's
enabling condition checks whether it has the focus.  The *focus*
variable is reassigned each time a different console task is
activated.  See *piety/run_ed* for a programming example.

### Shell ###

The *pysht* module defines a function *mk_shell* that accepts
configuration settings and returns a command function that can be
passed to the *Console* constructor, to make that *Console* instance
into a Python shell.

### Terminal ###

The *terminal* module contains platform-dependent functions used by *console*.

### Modules ###

These are the modules in the *piety* directory.  For more details see
their docstrings.

- **piety**, scheduler, defines *Task* class and *run* function

- **console, ascii, ansi**, skeleton command line application

- **pysht**, Python shell, configures *console* to provide
    a Python interpreter.

- **terminal**, utilities used by *console*

