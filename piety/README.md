piety
=====

The **piety** directory contains the Piety scheduler and job control
modules.

### Scheduling philosophy ###

Piety runs in a single Python interpeter session.  All Piety software,
including both operating system and applications, executes in this
session.  The session might run on a host operating system or on a
bare machine (with the minimum of hardware support in C or assembler).
There are only a few platform-dependent modules.  Most modules
developed for Piety on a host operating system should also work on a
bare machine.

Piety is event-driven.  Each Piety task identifies an *event*, a
*handler*, and an *enabling condition*.  A handler can be any Python
callable, including a function, method, generator, or coroutine.  An
enabling condition can be any callable that returns a Boolean.  The
scheduler is an event loop that may call a task's handler when its
event occurs and its enabling condition is true.  Then the handler
runs until it returns control to the scheduler.  There is no
preemption.  This is called *cooperative multitasking*.

In order run under the Piety scheduler as a Piety *application*, a
program (Python module or modules) must be organized as a collection of
functions or methods (etc.) that can be called as handlers.  It is the
programmer's obligation to ensure that each handler finishes quickly
enough for acceptable performance.  Many existing Python applications
are not designed to cooperate in this way --- instead they take over
the Python session, postponing all other tasks.  However, it may be
possible to adapt some of them.

The following sections describe the modules in the *piety* directory.

### piety.py ###

The *piety* module defines the *Task* class and schedules multiple
tasks in a single Python interpreter session.  

To run the Piety operating system: start Python, import the *piety*
module, create some *piety.Task* instances, then call *piety.run*.
One of the tasks can be a Python shell, so you can continue to
interact while Piety is running.  See the examples in the *scripts*
directory.  More details appear in docstrings.

A task runs an application.  To create a task for an application,
pass the application's handler when you create the task instance.
(Applications do not depend on the Piety scheduler, so they can also
run in an ordinary Python session.)

A Piety application must not block waiting to read input.  The *piety*
scheduler for Unix hosts uses the Unix *select* function to ensure
that the scheduler only calls handlers when there is input ready to
read.

### session.py ###

The *session* module provides the *Session* class that manages
multiple *jobs* in a single Piety task.  *Session* is a subclass of
*Task*.

More than one application can have a handler for the same event.
Those applications are called *jobs*.  For some events, it is
necessary that only one job handle each event.  That job has the
*focus* for that event.  The *Session* class manages the focus for
such events, multiplexing the event among the jobs that handle it.
A Piety session includes a *Session* instance for each event 
that must be shared among a group of jobs.

Sessions and jobs were motivated by terminal applications.  For
example, the Python shell and other terminal applications (editors
etc.) alternate, using the same terminal.  There is a single *Session*
instance for each terminal.  Each job in a session can be be suspended
and then resumed later without losing work in progress.

### job.py ###

The *job* module 

### command.py ###

The *command* module contains a skeleton command line application.  It
defines a class *Command*, with a *handle_key* method that gets a
single character typed at the command keyboard, and adds it to a
command line (usually).  When *handle_key* gets a line terminator
character, it calls a command function and passes the command line to
it.  The *handle_key* method also handles some editing functions and
other control keys.

The command function is passed as an argument to the *Command*
constructor, so this same class can act as the front end to any
command line application.  The command function can invoke the Python
interpreter itself, so a *Command* instance can act as Piety's Python
shell.

The Command *handle_key* method is usually called by the *getchar*
method in the *key* module.  It is this *getchar* method that is the
console task's handler, that is invoked by the Piety scheduler.

Revised January 2015

