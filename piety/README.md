
piety
=====

The *piety* module is the core of the Piety operating system.  It
defines the *Task* and *Session*. It imports the
*cycle* module and the *eventloop* module, which defines *run*,
the non-blocking event loop.  To run tasks in Piety, import the
*piety* module, create some *piety.Task* instances, then call
*piety.run*.  If one of the tasks is a Python shell, you can use it to
create or delete tasks while Piety is running.

This page provides an overview of tasks in Piety,
describes the classes in the *piety* module, describes the
Piety *run* function, and explains how it uses the *cycle* and *eventloop*
modules.

### Tasks in Piety ###

Piety runs in a single Python interpeter session.  All Piety software,
including both operating system and applications, executes in this
session.  The session might run on a host with a general-purpose
operating system, or on a bare machine running only a Python
interpreter.

Piety is event-driven.  A Piety session runs an event loop
that invokes *tasks*.  Each Piety task identifies an *event*, a
*handler*, and an *enabling condition*.  A handler can be any Python
callable: a function or method, etc.  The enabling condition can be
any callable that returns a Boolean.  A Piety event loop may call a
task's handler when its event occurs and its enabling condition returns
*True*.  Then the handler runs until it returns control to the event
loop.  There is no preemption.  This is called *cooperative
multitasking*.

A Piety handler must not block waiting for input (or other events).
The event loop only calls a handler when there is input ready to read
(or the awaited event has occurred).  This is called a *non-blocking*
event loop.

In order run as a Piety *application*, a program (Python module or
modules) must be organized as a collection of functions or methods
(etc.) that can act as handlers.  It is the programmer's
obligation to ensure that each handler finishes quickly enough for
acceptable performance.  Many existing Python applications are not
designed to cooperate in this way --- instead they take over the
Python session, postponing all other tasks.  However, it may be
possible to adapt some of them.

The following sections describe classes in the *piety* module.  For
much more information read the docstrings and comments the *piety*
module, and study the examples in the *scripts* directory.

### Task class ###

*Task* connects an application to the event loop.  Assign the
application's handler function (or method etc.) to the task object's
*handler* attribute to invoke the application from the event loop.

### Session class ###

*Session* is a subclass of *Task*.  A *Session* instance manages
multiple *jobs* in a single task.

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
instance for each terminal.  Each job (terminal application) in a
session can be stopped and then resumed later without losing work
in progress.  *Session* could also work with other kinds of jobs (besides
terminal applications).

### Jobs ###

A *job* class wraps an application to provide a standard interface
that enables *Session* (or another job control facility) to start,
run, and stop it, along with other applications.  The interface
includes the handler that the job uses to collect input and execute
commands, and the callables it uses to start (or resume) and stop (or
pause).  

The *Console* class defined in *console/console.py* is the *job* class
for terminal applications.  The module *scripts/session.py*
demonstrates how to connect *Console* jobs to a *Session* instance.
Applications that use other events (than terminal input) require
another job class.

The *Job* Enum represents the states a job can be in.

### Event Loop: run function, eventloop and cycle modules ###

The *run* function in the *piety* module is the non-blocking event
loop for a Piety session.  

The *run* function is not defined inline in the *piety* module.  Instead,
*piety* imports *run* from a separate *eventloop* module.  This
enables the platform-independent *piety* module to use different
*eventloop* modules.  The *eventloop* modules can be
platform-dependent, so they are not present in this directory.

There are several *eventloop* modules in different directories.  The
event loop in *select/eventloop.py* uses the Unix *select* call.
Another event loop in *asyncio/eventloop.py* uses the Python 3
*asyncio* module.  (Under the *python2* tag there is a
*twisted/eventloop.py* that uses the Twisted reactor.)  Piety imports
the *eventloop* module from the directory that is on the *PYTHONPATH*.
Commands in the *bin* directory put one or another directory on the
path.

The *piety* module imports *eventloop*.  Both modules import the
*cycle* module in this directory.  The platform-independent
*cycle* module avoids duplicating code in the *eventloop* modules
and separates the platform-independent code in this directory from 
platform-dependent code in the *eventloop* modules.
 
Revised Jan 2018
