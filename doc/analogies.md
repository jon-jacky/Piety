
Operating System Analogies in Piety
===================================

Piety is an operating system, but it is not like a conventional
operating system such as Linux or Windows.  Instead, our whole world
--- the entire computer system that Piety manages --- is a single
long-running Python session and its contents.  We make no attempt to
code something like Linux, but using Python instead of C
(as attempted [here](https://github.com/jtauber/pyv6)).   
Instead we do something quite different: we code the facilities needed to 
operate a simple personal computer, including its applications, all within 
a single Python session.  The result does not much resemble a conventional 
operating system, but we can still identify some analogies between 
conventional operating system concepts and the Piety system.

For now, Piety runs in an ordinary Python session running in a
terminal on a host computer.  At this stage, Piety depends on the
host operating system code running outside the Python session to
provide access to the terminal and the file system.  A long-range goal
of the Piety project is to replace the host operating system with code
that runs in a Python session on an otherwise bare machine.

In the meantime, we avoid using the host operating system as much as
we can.  Our short-term goal is to create and run Python code entirely
within Piety, using in-memory data structures instead of the host file
system, and using multiple windows in our single terminal instead of
the host desktop.  This will enable Piety development to be largely
self-hosted within the already existing Piety system.

This is how some traditional operating system contructs are realized in Piety:

- **task**: In Piety, a collection of functions (or methods or
any other callables) that can be invoked by a single kind of event
(keyboard input, periodic timer, etc.).  In Piety, functions that
are invoked by events are called *handlers*.  Piety runs an *event
loop* that detects events and invokes their handlers.  Each handler
should be *non-blocking*; it should exit promptly before the next
event (of any kind) occurs --- this is *cooperative multitasking*.
Handlers are not pure functions; most have side effects such as
updating editor buffers and display windows.  A task can include
several *jobs*.  More details [here](../piety/README.md).

- **process**: Piety does not have processes,
just tasks in a single address space.  When Piety runs on a host
operating system, the entire Piety session runs in a single host process.

- **background task**: a task whose handlers are invoked by
events that are not under the user's direct control, such as
a periodic timer.

- **concurrency**: In Piety, when two or more tasks that handle
different kinds of events are loaded into the system, each kind of
event might invoke a handler from a different task.  In this way,
tasks can interleave --- this is *interleaving concurrency*.
Interleaving tasks may alternate many times per second, providing an
illusion of parallelism.

- **parallelism**: Piety does not support true parallelism, where
different tasks run at the same time on different processors.

- **context save/restore**: In Piety, every handler runs to completion
and all data persists in the long-running Python session, so no
context save/restore is needed when different tasks run.

- **application**: Software that a user can run to perform some activity.
Editors and shells are examples of applications.  An application can run
as a standalone program in its own Python session, or it can be adapted to
run as a non-blocking task or job in a Piety session.
A typical Piety session has a shell and editor loaded, and perhaps some
other applications.   There are no barriers between applications
in a Piety session -- the functions and data in each
are accessible to all the others.

- **job**: a single application within a task.  A task can contain
multiple jobs.  The jobs within a task do not interleave with each
other (although they can interleave with other tasks).  Instead, one
job runs in the foreground while other jobs are suspended.  Suspended
jobs can be resumed.

- **terminal session**: a task whose handlers are invoked by keyboard
input.  A terminal session can include several console jobs.

- **console job**: a single application in a terminal session.
  Piety provides a [console](../console/README.md) module that
  adapts a terminal application to run as a console job.

- **foreground job**: the job that is handling a task's events.  In a
    terminal session, the application that is currently running on the
    terminal.

- **background job**: the job that will resume when the foreground job
    exits or is suspended.  In a terminal session, a shell is
    usually the background job when another application is running.

- **shell**: In Piety, a console job that provides a Python REPL
(Read-Evaluate-Print Loop).  In Piety, Python itself is the shell
command language.  However, the standard Python interpreter cannot
serve as the Piety shell because it blocks while waiting for the
next statement, which would prevent other tasks from running.  Piety
provides a simple callable Python shell named *pysh*
(rhymes with *fish*), along with [modules](../shells/README.md)
that adapt it to run in Piety sessions.  Piety also provides a more
elaborate shell named *wyshka* that makes it easy to alternate between Python
and an application command language, and provides redirection of the output of
any Python or application command.

- **memory management**: including allocation and reclamation (that is,
garbage collection).  Provided by Python language runtime.

- **memory protection**: The Python language itself prevents
corruption of its memory from programming errors (or deliberate
attacks) such as buffer overflows, etc.  Invalid list indices
etc. just raise exceptions; they do not overwrite other objects.  BUT there
is no access protection; any object can access any other object in the
Python session.

- **user accounts, multiuser operation**: No access controls
are possible within a single Python session, so Piety does not support
these.  Piety is a single-user system.

- **files**: We try to avoid using the host file system.  Instead, we
use in-memory data structures that can persist through the
long-running Python session.  In particular, we use text buffers,
instances of the *Buffer* class used in *ed.py*
and other editors.  They provide a *write* method so Python *print*
statements can write into them.  We will configure Python *import* to import
directly from these buffers so they don't need to be saved in the host
file system. (Not yet implemented)

- **i/o redirection**: In Piety, redirecting the output of
a task to some text buffer.  Redirection is provided by the *wyshka* shell.

- **desktop, window manager**: Our display editors *edda* and *edsel*
provide multiple tiled windows in a
single terminal, where each window displays (part of) the contents of
a text buffer.  The display module *frame* used by these editors does
not depend on *edsel* or any other application so it is in effect a
separate window manager; it can display windows that are updated by
different applications.

- **boot**: start the standard blocking Python interpreter, import
Piety operating system and application modules, start Piety event
loop, start non-blocking Piety Python REPL console job.  Optionally,
start other applications.  This can all be accomplished by a Python
script.  The Piety *scripts* directory contains several Python modules
that boot Piety in different configurations.

- **shutdown**: Optionally, stop applications.  Then exit non-blocking
Python REPL console job and return to standard blocking Python
interpreter, stop Piety event loop, exit Python.

- **virtual machine**: On a conventional operating system, it is possible
to use a *virtual machine monitor (VMM)* (or *hypervisor*)
such as QEMU or VirtualBox to run another operating system in a *virtual machine*.
Piety only uses Python, so a Python interpreter is the only
VMM needed to run Piety.  The Python session is the entire virtual machine.

- **kernel mode**: Piety does not distinguish kernel and user modes.
All code, including applications, runs with the same privileges.

The operating system that Piety resembles the most is
[Oberon](http://www.projectoberon.com/).  Oberon uses cooperative
multitasking, uses a text buffer class as a building block, and uses a
multiwindow text editor as its desktop and system shell.

Revised Jan 2020

