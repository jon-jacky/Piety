
Piety
=====

**Piety** is a notional operating system to be written in Python.

[Introduction](#Introduction)  
[Project Status](#Project-Status)  
[Roadmap](#Roadmap)  
[Dependencies](#Dependencies)  
[Python Versions](#Python-Versions)  

## Introduction ##

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
simple but self-contained personal computer operating system,  Let's  see
how far we can get with just Python. There is already a lot of work by
others that we might be able to use or adapt (see
[doc/utilities.md](doc/utilities.md)).

An overview of the Piety design appears [here](doc/analogies.md).  There is
a [script](scripts/demo.py) that demonstrates many Piety features,
described [here](scripts/demo.md).   Another page describes the Piety
[directories](DIRECTORIES.md) and their contents. Ongoing and recent work
on Piety is described [here](BRANCH.md).

## Project Status ##

For now, Piety runs in an ordinary Python interpreter session on a host
operating system.   At this stage, the experiment is to see if it can be
possible to create, edit, and run Python modules completely within a
single Python session, without resorting to the host desktop or command
line.  In the present configuration, the user interface to Piety is
[edsel](editors/edsel.md), a combined  display editor, shell, and window
manager, which together provide a minimal but self-contained programming
environment within a single Python terminal session.

I hope someday to run Piety on a bare machine with no other
operating system, but only a Python interpreter with minimal support.
There are only a few platform-dependent modules.  Most modules developed
for Piety on a host operating system should also work on a bare machine.

## Roadmap ##

There is no roadmap -- no plan for a sequence of steps to bring Piety
to some pre-defined state of completion.

Piety is a personal project and I have no expectation to make it generally
useful.  I have brought Piety to its present state by working  in short
bursts on an irregular schedule, when I can find the time and interest.  I
decide what to work on next as I go along.  I often go back and rewrite
what I have already done, to make it easier to work with or just to
improve the style.

There is no roadmap, but the project divides naturally into two parts,
corresponding to the user space and the kernel of a conventional operating
system.  The user space of Piety is the programming environment that runs
in a Python terminal session hosted on any conventional operating system.
All the work I have done so far is in this part. The kernel of Piety is
the part that replaces the kernel of a conventional operating system,
including just enough C or assembler code to start the Python interpreter and
connect it to the hardware, and then Python for most of kernel including
device drivers and file system.  I have not even begun this part.
It would require a more concentrated, sustained effort than I have  been
able to make so far.

It is likely that work in the near future will continue in the user space.
I can always add features and improve the convenience of the programming
environment.  I might also add other applications, for example a simple
text-only web browser in pure Python.  I would observe the discipline that
any applications must be developed completely within the Piety programming
environment.

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

Revised Apr 2022

