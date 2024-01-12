
Piety
=====

**Piety** is a notional operating system to be written in Python.

[Motivation and Goals](#Motivation-and-Goals)  
[Current Status](#Current-Status)  
[Roadmap](#Roadmap)  
[Dependencies](#Dependencies)  
[Python Versions](#Python-Versions)  
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

For now, Piety runs in an ordinary Python interpreter session on a host
operating system.   Here is an explanation of the Piety
[design](doc/analogies.md).


At this time, Piety provides [cooperative multitasking](piety/README.md),
[jobs](scripts/session.md) that can be suspended and resumed, a Python-
based [shell](shells/wyshka.md) with output redirection,  a [line
editor](editors/ed.md), and a [display editor](editors/edsel.md). 

The display editor includes a built-in shell and window manager, which
together provide a minimal but self-contained programming environment
within a single Python terminal session.  It is the programmer's user
interface to the Piety system.  It provides the CPython interpreter,
which can be invoked in
[several ways](editors/edsel.md#Writing-and-running-Python-in-edsel).

There are some small [samples](samples/README.md) and
[scripts](scripts/README) for demos and testing.  This
[demo](scripts/demo.md) exhibits many Piety features.

Other pages describe the Piety [directories](DIRECTORIES.md) and their
contents, and its [modular structure](doc/modules.md).

NOTE: The preceding paragraphs describe the Piety version in the
*master* branch, labelled with the *version1* tag.  Work on this
version ended in Jan 2023.  A total rewrite is now underway in the *rewrite*
branch, to simplify the code and improve its organization and clarity.
It might be quite a while before the code in *rewrite* provides
equivalent functionality to *master*.

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

A history of some of this past work appears [here](BRANCH.md) (it omits
the early years).

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
in the hosted part.  I have researched [several
approaches](doc/baremachine.md) to building the native part, but have not
begun work on any.   Every approach would require a more concentrated,
sustained effort than I have been able to make so far.

It is likely that work in the near future will continue in the hosted part.
I can always add features and improve the convenience of the programming
environment.  I might add other hosted applications, for example a simple
text-only web browser in pure Python.  

At this stage, the experiment is to see if it can be possible to create,
edit, and run Python code using only the programming environment we have
built so far, without resorting to the host desktop or command line.

I will try to observe the discipline that Piety is *self-hosted*: any new
Piety code must be developed within its already existing programming
environment.

NOTE: At this writing (Feb 2023) a total rewrite is underway in the
*rewrite* branch, to simplify the code and improve its organization
and clarity.

## Dependencies ##

The Piety system has no dependencies, other than Python itself
(including a few standard library modules).  This makes Piety a
minimal self-contained system, written in a uniform style throughout.
Alternatively, it might be possible to assemble similar functionality
from [other projects](doc/utilities.md), but I expect the resulting
system would be larger and harder to understand than Piety.

## Python Versions ##

Piety is written in Python 3 since June 2015.   Earlier work is saved in
this repository in the *python2* tag.  The conversion is described
[here](doc/python3.md).   Piety now requires Python 3.5.

## Tested Platforms ##

Through November 2023, the Piety software only ran on one computer: a
MacBook Pro (13 inch, early 2011), running Mac OS (through 10.11.6 El
Capitan, the most recent version that runs on that hardware).    It
only ran in the Mac OS Terminal, through version 2.6.2 (361.2). It
only ran on CPython downloaded from python.org, through version 3.9.0.

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

Revised Jan 2024

