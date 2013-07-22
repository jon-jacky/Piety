
Piety
=====

**Piety** is a notional operating system to be written in Python.  It
is a response to this impulse:

> *Today's operating systems and applications are bloated and
> complicated.  Let's start over, and create a complete system that is
> small, easy to understand, and fun to program.  And, let's build it
> all in our favorite language!*

We draw inspiration from the single-user, single-language,
special-hardware computers of the 1970s and 80s: Smalltalk, Lisp
machines, Oberon (see [doc/precursors.md](doc/precursors.md)).  Piety
is an experiment to see if we can achieve something similar today with
Python, but running on ordinary hardware.

We aim to produce, in Python, a minimal system capable of --
what else? -- writing and running Python programs.  This requires only
a text console, a Python interpreter, an editor, and a file system.
We also hope to experiment with TCP/IP networking (including the web)
and graphics.  We aim to see how far we can get with just Python.

For now Piety runs in any ordinary Python interpreter session.  We
hope someday to run Piety on a bare machine with only a Python
interpreter (and perhaps a few minimal interrupt handlers written in C
or assembler).

Recent projects by others in a similar spirit include
[PyCorn](http://www.pycorn.org/home) and
[Cleese](https://github.com/jtauber/cleese/) in Python, and
[STEPS](http://www.vpri.org/pdf/tr2011004_steps11.pdf) in other
languages.

This repository contains some notes and experiments in these
directories:

- **doc**, notes and documents

- **piety**, scheduler

- **samples**, samples to run under the scheduler 


