
Piety
=====

**Piety** is an operating system written in Python.

[Motivation and Goals](#Motivation-and-Goals)  
[Current Status](#Current-Status)  
[Roadmap](#Roadmap)  
[Dependencies](#Dependencies)  
[Tested Platform](#Tested-Platform)

## Motivation and Goals ##

Piety is a small but self-contained personal computer operating system for
programmers.  It provides a responsive and malleable platform for writing
and programming.  Its internals are easy to understand and modify.
 
Piety uses a single programming language -- Python -- for both the
applications and the operating system. You can use the language interpreter
to inspect and manipulate any data in the running system.  Changes to
application and system code are effective immediately, without having to
stop and restart the system.

Piety is a reaction against the complexity and disempowerment of today's
dominant computer systems.  I take inspiration from the single user, single
language, special hardware systems of the 1970s and 80s: Smalltalk, Lisp
machines, Oberon (see [doc/precursors.md](doc/precursors.md)).     Piety is
an experiment to see if I can put together something similar today, but
using a familiar programming language running on ordinary hardware.  Let's
see how far we can get with just Python. There is already a lot of work by
others that we might be able to adapt or use as models (see
[doc/utilities.md](doc/utilities.md)). For other projects in a similar
spirit, again see [doc/precursors.md](doc/precursors.md).
  
## Current Status ##

For now, Piety runs in an ordinary Python interpreter session in a single
terminal on a host operating system.   The Python interpreter with its runtime
is the virtual machine where the Piety OS now runs, analogous to the QEMU
virtual machine in many other operating system projects.

Piety provides a [display editor](editors/README.md),  and a 
[custom Python interpreter](tasking/pyshell.py). The display editor can support 
multiple buffers and windows in the terminal, and also a region for the
Python interpreter. Together these provide a minimal but self-contained
programming environment within a single Python terminal session.

Piety development is self-hosted in this programming environment.  Code is
added and revised in a long-running Python session.  Code  is imported and
reloaded into the session without restarting or  losing work in progress.
To make this possible we adopted a
[particular workflow and coding style](editors/HOW.md).

Piety provides concurrency with a Python *asyncio* event loop.  Tasks 
are implemented by Python *coroutines* or *readers* (event handlers) that
run in an event loop.

Piety provides *asyncio* readers for its custom Python shell and its
editor.  These enable the shell and the editor to run without 
blocking in an event loop, so other tasks can run concurrently, as you 
type commands in the shell or edit text in the editor.  

The editor is not just for creating text. Python commands including
concurrent tasks can redirect their output to editor buffers and windows, so
the editor can be used for data capture and animated display.  We
use it for [experiments](piety) in tasking and concurrency
where tasks update windows as we control their behavior by typing  commands
at the Python interpreter.

Here is more about some Piety [design decisions](doc/rationale.md) and their
rationales.

We don't have any screenshots or animations, but if we did, they would show
the scenarios described in *piety/pmacs_script.md* and *pmacs_blocking.md*.
For now, you can just read along there and do the demos yourself.
   
The present version of Piety was started from scratch in February 2023.  Its
development is ongoing here in the *rewrite* branch of the *Piety* repository.
An archive of the earlier version of Piety that was abandoned in January 2023
is here in the  *master* branch and *version1* tag.  The *rewrite* branch
is now the main branch; I will  never merge it back into *master*.
     
## Roadmap ##

I hope someday to run Piety on a bare machine with no other
operating system, but only a Python interpreter with minimal support.

Piety divides naturally into two independent parts: the *hosted* part and
the *native* part.  The hosted part can run in any Python interpreter. It
includes the editors, shells, tasking, the  programming environment,
and any tools and applications we might write.  The native part includes the
Python interpreter itself, and the support needed to run the interpreter  on
the computer hardware.   Almost any general-purpose operating system can
serve as the support, but the goal is to replace that with a special-purpose
operating system which is itself mostly written in Python.

All the work I have done so far, including the programming environment, is
in the hosted part.  I have researched 
[several approaches](doc/baremachine.md) to building the native part, but
have not yet started work on any.   I hope to begin soon.
 
## Dependencies ##

The Piety system has no dependencies, other than Python itself
(including a few standard library modules).  This makes Piety a
minimal self-contained system, written in a uniform style throughout.
Alternatively, it might be possible to assemble similar functionality
from [other projects](doc/utilities.md), but I expect the resulting
system would be larger and harder to understand than Piety.

## Tested Platforms ##

Through November 2023, the Piety software was only
run on one computer: a MacBook Pro (13 inch, early 2011), running Mac OS
(through 10.11.6 El Capitan, the most recent version that runs on that
hardware). It ran in the Mac OS Terminal, through version 2.6.2 (361.2). It
ran on CPython downloaded from python.org, through version 3.9.0.

Beginning in December 2023, Piety development moved to Linux
running in a virtual machine on a Chromebook.  The *uname -a* command
says it is *Linux penguin 5.15*, which I believe is a Chromebook fork of
Debian. This is the Linux provided to ordinary users as part
of the standard Chromebook software, it is not part of some 'developer
mode'.   The Python running in this Linux is CPython version 3.9.2.
Piety runs in the Chromebook Linux Terminal app.
The Chromebook itself is a Lenovo Ideapad 3 Chrome  14M836
purchased in April 2023.  At this writing (12 Jan 2024) it is running
ChromeOS Version 118.0.5993.164.

Revised Aug 2024

