
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
Python, but running on ordinary hardware.

We aim to produce, in Python, a simple but self-contained personal
computer operating system capable of -- what else? -- writing and
running Python programs.  A minimal system requires only a text
console, a Python interpreter, some standard library modules, and
persistent storage (not necessarily a file system).  We also hope to
experiment with TCP/IP networking (including the web) and graphics.
We aim to see how far we can get with just Python.  There is already a
lot of work by others that we might be able to use or adapt (see
[doc/utilities.md](doc/utilities.md)).

Piety might be used for ---

- **Education** - Exhibit and explain almost all of the code for an
    entire system, expressed in a readable high-level language (as
    they did for
    [Oberon](http://www.inf.ethz.ch/personal/wirth/ProjectOberon/)).
    Use the Python interpreter to inspect and manipulate any data
    structures in a running system.

- **Research** - Experiment with new or unconventional operating
    system constructs (like the alternative to the file system
    proposed for [Gracle](https://github.com/jon-jacky/Piety/blob/master/doc/gracle_excerpts.txt)).

- **Embedded computing** - Run standalone Python applications on minimal platforms (something like [PyMite](https://wiki.python.org/moin/PyMite) or [Micro Python](http://micropython.org/)).

- **Cloud computing** - Run Python applications on virtual machines, minimizing resource consumption and startup time (as in [Mirage](http://www.openmirage.org/), [HalVM](http://corp.galois.com/blog/2010/11/30/galois-releases-the-haskell-lightweight-virtual-machine-halv.html), [Erlang on Xen](http://erlangonxen.org/), and [OSv](http://osv.io/)).

For now, Piety runs in an ordinary Python interpreter session on a
host operating system.  We plan to run Piety on a bare machine (or
bare VM) with no other operating system, but only a Python interpreter
(with the minimum of hardware support in C or assembler).  There are
only a few platform-dependent modules.  Most modules developed for
Piety on a host operating system should also work on a bare machine.

Recent projects by others in a similar spirit include
[PyCorn](http://www.pycorn.org/home) and
[Cleese](https://github.com/jtauber/cleese/) in Python, and
[STEPS](http://www.vpri.org/pdf/tr2011004_steps11.pdf) in other
languages.

The Piety modules are organized into these [directories](directories.md)

Revised February 2015


