
Piety
=====

**Piety** is a notional operating system to be written in Python.

[Motivation and Goals](#Motivation-and-Goals)  
[Current Status](#Current-Status)  
[Roadmap](#Roadmap)  
[Dependencies](#Dependencies)  
[Tested Platform](#Tested-Platform)

## Motivation and Goals ##

Piety is a response to this impulse:

> *Today's operating systems and applications are bloated and
> complicated.  Let's start over, and create a complete system that is
> small, easy to understand, and fun to program.  And, let's build it
> all in our favorite language!*

I am intrigued by the single user, single language, special hardware
systems of the 1970s and 80s: Smalltalk, Lisp machines, Oberon (see
[doc/precursors.md](doc/precursors.md)).   Those systems used a single
programming language for both the applications and the operating system.
You could use the language interpreter to inspect and manipulate any data
in the running system.  Changes to application and system code were
effective immediately, without having to stop and restart the system.

Piety is an experiment to see if I can put together something similar
today, but using a familiar programming language running on ordinary
hardware. (For other projects in a similar spirit, again see
[doc/precursors.md](doc/precursors.md).)  I aim to produce, in Python, a
simple but self-contained personal computer operating system.  Let's  see
how far we can get with just Python. There is already a lot of work by
others that we might be able to use or adapt (see
[doc/utilities.md](doc/utilities.md)).

## Current Status ##

For now, Piety runs in an ordinary Python interpreter session in a single
terminal on a host operating system. 

Piety provides a [display editor](editors/README.md),  and a 
[custom Python interpreter](tasks/pyshell.py). The display editor can support 
multiple buffers and windows in the terminal, and also a region for the
Python interpreter. Together these provide a minimal but self-contained
programming environment within a single Python terminal session.

The editor is not just for creating text. Python commands including
concurrent tasks can redirect their output to editor buffers and windows, so
the editor can be used for data collection and animated display.  We have
used it for [experiments in tasking and concurrency](tasks/README.md),
where tasks update windows as we control their behavior by typing  commands
at the Python interpreter.

Piety development is self-hosted in this programming environment.  Code is
added and revised in a long-running Python session.  Code  is imported and
reloaded into the session without restarting or  losing work in progress.
To make this possible we adopted a
[particular workflow and coding style](editors/HOW.md).

The present version of Piety was started from scratch in February 2023.  Its
development is ongoing here in the *rewrite* branch of the *Piety* repository.
An archive of the earlier version of Piety that was abandoned in January 2023
is here in the  *master* branch and *version1* tag.
     
## Roadmap ##

This project is a series of experiments. There is no plan for a sequence
of steps to bring Piety to some completed, finished state.  Instead, here
are some notes about my working method, and some experiments I might try
in the future.

I have brought Piety to its present state by working  in short
bursts on an irregular schedule, when I can find the time and interest.  I
decide what to work on next as I go along.  I often go back and rewrite
what I have already done, to make it easier to work with or just to
improve the style.

A history of some of this past work appears [here](BRANCH.md).

I hope someday to run Piety on a bare machine with no other
operating system, but only a Python interpreter with minimal support.

Piety divides naturally into two independent parts: the *hosted* part and
the *native* part.  The hosted part can run in any Python interpreter. It
includes the applications, shells, job control, tasking, and the
programming environment. The native part includes the  Python interpreter
itself, and the support needed to run the interpreter  on the computer
hardware.   Almost any general-purpose operating system can serve as the
support, but the goal is to replace that with a special-purpose operating
system which is itself mostly written in Python.

All the work I have done so far, including the programming environment, is
in the hosted part.  I have researched 
[several approaches](doc/baremachine.md) to building the native part, but
have not begun work on any.   Every approach would require a more
concentrated, sustained effort than I have been able to make so far.

It is likely that work in the near future will continue in the hosted part.
Until now, we have only experimented with tasks implemented by Python
threads. Next, we expect to try experiments with coroutines implemented by
Python generators, and after that, we may experiment the Python *asyncio*
library.
 
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
purchased in 2023.  At this writing (12 Jan 2024) it is running
ChromeOS Version 118.0.5993.164.

Revised May 2024

