
Piety
=====

**Piety** is a notional operating system to be written in Python.  It
is a response to this impulse:

> *Today's operating systems and applications are bloated and
> complicated.  Let's start over, and create a complete system that is
> small, easy to understand, and fun to program.  And, let's build it
> all in our favorite language!*

We draw inspiration from the single-user, single-language,
special-hardware systems of the 1970s and 80s: Smalltalk, Lisp
machines, Oberon (see [doc/precursors.md](doc/precursors.md)).  Piety
is an experiment to see if we can achieve something similar today with
Python, but running on ordinary hardware.  (For other projects in a 
similar spirit, again see [doc/precursors.md](doc/precursors.md).)
We aim to produce, in Python, a simple but self-contained personal
computer operating system.
We aim to see how far we can get with just Python.  There is already a
lot of work by others that we might be able to use or adapt (see
[doc/utilities.md](doc/utilities.md)).

For now, Piety runs in an ordinary Python interpreter session on a
host operating system.  An overview of its design appears
[here](doc/analogies.md).  We have a [script](scripts/run_timestamps.py) that
demonstrates many Piety features, described
[here](scripts/run_timestamps.md).  We plan to run Piety on a bare
machine (or bare VM) with no other operating system, but only a Python
interpreter with minimal support.
There are only a few platform-dependent modules.  Most modules
developed for Piety on a host operating system should also work on a
bare machine.

Piety might be used for ---

- **Education** - Exhibit and explain almost all of the code for an
    entire system, expressed in a readable high-level language (as
    they did for [Oberon](http://www.projectoberon.com)).
    Use the Python interpreter to inspect and manipulate any data
    structures in a running system.

- **Research** - Experiment with new or unconventional operating
    system constructs (like the alternative to the file system
    proposed for [LispOs](https://github.com/robert-strandh/LispOS).

- **Embedded computing** - Run standalone Python applications on minimal platforms (something like [PyMite](https://wiki.python.org/moin/PyMite) or [Micro Python](http://micropython.org/)).

- **Cloud computing** - Run Python applications on virtual machines, minimizing resource consumption and startup time (as in [Mirage](http://www.openmirage.org/), [HalVM](http://corp.galois.com/blog/2010/11/30/galois-releases-the-haskell-lightweight-virtual-machine-halv.html), [Erlang on Xen](http://erlangonxen.org/), and [OSv](http://osv.io/)).

Another page describes the Piety [directories](DIRECTORIES.md) and
their contents.

An overview of the Piety design appears [here](doc/analogies.md).

A [script](scripts/run_timestamps.py) that demonstrates many Piety
features is described [here](scripts/run_timestamps.md).

Ongoing and recent work on Piety is described [here](BRANCH.md).

The Piety system has no dependencies, other than Python itself
(including a few standard library modules).  This makes Piety a
minimal self-contained system, written in a uniform style throughout.
Alternatively, it might be possible to assemble similar functionality
from [other projects](doc/utilities.md), but we expect the resulting
system would be larger and harder to understand than Piety.

Piety is written in Python 3 since June 2015.  Earlier work is saved
in this repository in the *python2* tag.  The conversion is described
[here](doc/python3.md).

Revised May 2018
