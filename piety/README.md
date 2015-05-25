
piety
=====

The *piety* module defines *Task*, *Job*, *Session*, and *run* (the
non-blocking event loop).  It is the core of the Piety operating
system.  To run tasks in Piety, import the *piety* module, create some
*piety.Task* instances, then call *piety.run*.

The following sections first provide an overview of tasks in Piety,
then describe classes in the *piety* module, and finally explain
the Piety *run* function and how it can use different event loops.

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
task's handler when its event occurs and its enabling condition is
true.  Then the handler runs until it returns control to the event
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
much more information use *help(piety)* etc. and see the scripts in
the *scripts* directory, especially *console_tasks* and *piety*.

### Task class ###

*Task* connects an application to the event loop.  Assign the
application's handler function (or method etc.) to the task object's
handler attribute to invoke the application from the event loop.

### Session class ###

*Session* is a subclass of *Task*.  A Session instance manages
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
instance for each terminal.  Each job in a session can be be suspended
and then resumed later without losing work in progress.

### Job class ###

The *Job* class provides a uniform interface (with known method names) to the
application for the *Session*'s job control. *Job* also uncouples
*Session*'s scheduling and job control from any particular device or
event (such as the terminal). Therefore its initializer has to
have a lot of arguments to access application methods.

### Event Loop ###

The *run* function in the *piety* module is the event loop for a Piety session.

The *run* function is not defined in the *piety* module.  Instead,
*piety* imports *run* from an *eventloop* module.  This enables
*piety* to use different event loops.  At this time the usual event
loop is in *select/eventloop.py*; it uses the Unix *select* call.  Another
event loop in *twisted/eventloop.py* uses the Twisted reactor.  Piety 
imports the *eventloop* module from the directory that is on the
*PYTHONPATH*.  Commands in the *bin* directory put one or another
directory on the path.

The *piety* module imports *eventloop*, but *eventloop* uses several
data structures defined in *piety*, including *schedule*.  The *piety*
module shares these by assigning them to attributes in *eventloop*
after it imports that module.
 
Revised May 2015

