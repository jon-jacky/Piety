
Design decisions and rationales
===============================

Some design decisions for Piety, and their rationales:

[Piety](..) is a small personal computer operating system for
programmers.

Piety uses a single programming language -- Python -- for both the
applications and the operating system.

Piety has no dependencies, other than Python itself.
 
Code is added and revised in a long-running Python session,  without
restarting or losing work in progress.

Piety provides concurrency with a Python *asyncio* event loop.

[Personal computer](#Personal-computer)  
[For programmers](#For-programmers)  
[Python](#Python)  
[No dependencies](#No-dependencies)  
[Operating system](#Operating-system)  
[Long-running session](#Long-running-session)  
[Small](#Small)  
[Concurrency with *asyncio*](#Concurrency-with-asyncio)  
 
### Personal computer ###

Piety is intended to support a truly *personal* computer, whose software
is created (or selected and modified) by its owner, to express their own
preferences and inclinations.  A personal computer enables its owner to work
-- or just pass the time -- in the way that is most comfortable and satisfying for
them, no matter how unusual or eccentric that might be.   Piety is a deliberate
reaction against the prevailing trend to try to build a system that everyone
will use, that will take over the world. 

### For programmers ###

I see Piety as an *activity*: a series of experiments, an
ongoing project. I often add features, but I am not trying to
make a finished product.
  
I resolved to write Piety from scratch, with no tools, starting from a
Python prompt in a terminal window. First, I made a simple text editor,
then used that to build the rest. I did write the first two hundred
lines or so -- a few pages -- in another editor, but after that Piety
development has been completely self-hosted in Piety itself.
Building Piety up from almost nothing was an essential part of the 
experience for me. It still informs all my use of the system.
 
I do not expect anyone else to use Piety routinely. It bears too many of
my own peculiar preferences, and limitations that are severe but
tolerable to me.  But other programmers  might try it out, or just look into 
the code and documents, to get ideas, techniques, and examples
they could use to build systems that express their own preferences.

### Python ###

Python is typically used from an interactive interpreter that enables the
user to inspect and modify the running session, including importing and
reloading entire modules.  Lisp and Smalltalk introduced this way of
working, and it is now provided by many other languages, but today Python is
ubiquitous and is most familiar to me.

Python already provides most of the operating system functionality that a
typical user sees.   Its interactive interpreter, along with its standard
libraries, can do everything a Unix shell can do.   Its generators and
coroutines provide concurrency.   Its standard libraries provide a network stack.
Many [examples](utilities.md) show how to do systems programming in Python.
And, thanks to its popularity and long history, there are Python libraries
and applications for almost anything you might want to do with a computer. 

Given all this, why do we need a user-facing operating system at all?
For now, we need it to run programs that are not in Python.  But this comes at 
the cost of adding many additional things you must know to use the computer.
Maybe we can simplify our computing life by dispensing with all that, and
just use Python for everything.

### No dependencies ###

Piety has no dependencies, other than the language and libraries included
in the standard Python distribution.

This makes development easy.  Python and its standard libraries come already
installed on every system I have used.  I do not need to set up any
Python environment, other than defining a single shell command to put the 
Piety directories on the PYTHONPATH.  I do not need to search the 
internet for packages and documentation.  Everything I need for Piety can
be found in the local Python installation, often by using the Python
*help* command.

This also makes it easy for others to try out Piety.  They can just
clone this Piety repository and use their system's built-in *python* (or
*python3*) command to run the scripts.
     
### Operating system ###

In a computer whose operating system is written in Python, almost all code
in the system, including the usual operating system functions as well as
applications, runs in the Python interpreter.  To boot the system, (almost)
the first thing we must do is start Python, which then runs everything else.
 
### Long-running session ###

An entire life cycle of the system from startup to shutdown runs in a single
Python session - a single long-running invocation of the Python interpreter.

To develop and use new software in a single long-running session, it must be
possible to import and reload a module without restarting the session or
losing work in progress.   Reloading a module must make new or revised
functionality available immediately, yet the state of the session -- the
values of all its variables -- must be preserved across reloads, including
the state of the reloaded module itself.

We preserve state across reloads by only initializing variables the first time
a module is imported, using the coding technique described in
[How we program](../editors/HOW.md#Reloading-modules).

 
### Small ###

Piety has to be small, because it is written by one person in his spare time.

I use existing Python language constructs and the standard library  instead
of writing new code as much as I can, even if that requires limiting
functionality and adopting a restricted programming style. I try to avoid
hard problems, or replace them with easier ones instead.

For example, the standard Python function *reload* does not update  existing
objects with their new definitions from the reloaded module.   There are
some complicated "hot reloading" packages that overcome this, but I just
accept the limitation, avoid using objects to store persistent application
data, and use dictionaries instead (again see
[How we program](../editors/HOW.md#Modules-and-dictionaries-instead-of-classes-and-objects))


### Concurrency with *asyncio* ###

Piety provides concurrency with a Python *asyncio* event loop.

I also considered the Python *threading* library (here are  some
[experiments](../threads)), but I rejected it because it uses
the host operating system's threading library.  My goal for Piety is to
replace the host operating system.
 
The *asyncio* library is all written in Python.  It is built on the Python
interpreter itself, based on generators and *yield*.  It seems it should be 
able to run without much support from the host operating system.

Concurrency using the *asyncio* event loop provides *cooperative multitasking*,
which requires a particular coding style.   Each task responds to events -- 
such as key presses -- and the code that handles each event runs to completion
before the system can handle other events or run other tasks.
Code must not *block* -- wait for events or data that are not yet available.

The Piety editor and Python shell are coded so they can run without blocking
in the event loop. Here is an
[explanation and demonstration](../piety/pmacs_blocking.md).

Revised Jul 2025

