
Operating System Analogies in Piety
===================================

Piety is an operating system, but it is not much like a conventional
operating system such as Unix or Linux.  

Instead, our whole world --- the entire computer system that Piety
manages --- is a long-running Python session and its contents.

We made no attempt to code something like Unix, but using Python
instead of C.  Instead we identify analogies between some conventional
operating system concepts and a system that runs entirely in a Python
session.

- **task**: collection of functions (actually, methods or any other
callables) that can be invoked by a single kind of event (keyboard
input, or timer expires, etc.).  In Piety, unctions that are invoked
by events are called *handlers*.  Each handler should exit before the
next event (of any kind) occurs --- this is *cooperative multitasking*.
Handlers are not pure functions, most have side effects such as updating
editor buffers and display windows.  A task can include several *jobs*.
More details [here](../piety/README.md).

- **terminal session**: a task whose handlers are invoked by keyboard
input.  A terminal session can include several console jobs.

- **application**: a conceptually unified service that provides a collection
of functions (or other callables) that can be invoked as a task or a
job.

- **job**: a collection of functions within a task that comprises a single
application.  

- **console job**: a single application in a terminal session.

- **background task**: a task whose handlers are invoked by a periodic timer.

- **concurrency**: two or more tasks that handle different events are loaded
into the system, so that each kind of event might invoke a handler
from a different task.  In this way, tasks can interleave.  Or,
several jobs are loaded, so that different events of the the same kind
might invoke a handler from a different job.

- **parallelism**: Piety does not support true parallelism, where different
tasks are executing simultaneously on different processors.

- **context save/restore**: everything persists in the always-running Python
session so no context save/restore needed.

- **memory management**: including allocation and reclamation (that is,
garbage collection).  Python language built-in runtime.

- **memory protection**: Python language built-in runtime prevents buffer
overflows, etc.   Invalid list indices etc. just throw exceptions, do not
overwrite other objects.  BUT there is no access protection, Python
can access any object in the session, that is, anything in the
"computer".

- **user accounts, multiuser operation**: No protection or access controls
are possible within a single Python session, so Piety does not support
these.  Piety is a single-user system.

- **files**: In Piety, much of the functionality of files is provided by
editor text buffers in memory.  For example we plan to do Python
*import* from a text buffer (not yet implemented).  (Maybe can expand
this into single-level store.  When running hosted, just read all the
buffers from host file system at Piety startup and store all in host
file system at Piety shutdown.  Then maybe add a checkpointing scheme
for crash/error protection.  When running in VM, no host files are
needed, all buffers are implicitly saved in and restored from the VM
image.)

- **desktop, window manager**: editor display and window commands
act as a tiling window manager.  The *frame* (display) module is separate from
any particular editor or other application so it is in effect a
separate window manager.

- **windows**: editor windows into different text buffers.  Different tasks
can write into different text buffers, all update in displayed windows
as updates appear.

- **i/o redirection**: reassign (monkey patch) Python *print*, to
print to any text buffer (not yet implemented). Reassign *stdout* to
write to any text buffers (not yet implemented). (These only work
because we do not have true parallelism, and we do have cooperative
multitasking.  We can always explicitly reassign *print* and *stdout* when we
switch tasks)

- **boot**: start Python, import needed modules from host file system, start
piety scheduler, start Piety Python REPL Console job.  Maybe start editor +
window manager, maybe load some editor buffers from host file system.
All this can be done from .py scripts, host file system can have
different scripts for different Piety configurations.

- **shutdown**: write editor buffers to host file system, exit Piety Python
REPL Console job, stop Piety scheduler, exit Python.

- etc, more analogies ...

Revised February 2018
