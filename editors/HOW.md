
How we program 
==============

We have all of our source code, our editors, and
the interactive Python interpreter always available in our
Python session.
We write code that we load and run immediately, without restarting
the session or losing any work in progress.

Our editors here -- [*sked*, *edsel*, and *dmacs*](README.md) --
were developed in this way.  The first two hundred
lines of *sked* were written in another editor and
then imported into an interactive Python session. 
After that, sked was developed incrementally
in the long running session.  We used *sked*
to edit its own source code, adding functions one or two 
at a time, then reloading the module into the same session,
using the new functions right away on the same source files.
Proceeding in the same way, we used *sked* to write *edsel*, and 
*edsel* to write *dmacs*.

To make this possible, we had to adopt a Python coding style
that has some unusual features.  The small collection of modules
here that we have written in this style comprise a Python programming 
environment which is minimal, even crude.  But we find
that its malleability and responsiveness
motivate us to continue working in it, despite its lack of conveniences.

The following sections describe some features of our programming style.

### No programs, applications, or command interpreters ###

We do all of our work in a long-running interactive Python session.
We do not run "programs" or "applications".  Instead, we type commands 
to the Python interpreter that import 
modules and call functions in those modules.  The function calls 
are transient, although the data they create can persist.
The function calls might take over the keyboard and screen
for a while, but the Python interpreter is often visible in part of 
the screen, and is always accessible with a keystroke or two.

We don't invent command languages or write command interpreters; 
we use Python for that.  The Python interpreter itself is the "main
program" that invokes the functions in the modules we write.

### Reload functions, not data ###

We frequently reload modules to add functions we have just written.
BUT we must do this in a way that that preserves all persistent data
including our work in progress.

Reloading a module simply executes all the statements in the module.
So it executes all the function definitions, which picks up new functions
and also redefines revised functions -- this is just what we want.
BUT it also executes the data definitions, which has the effect of 
re-initializing them -- which we do *not* want, since this would destroy
any data that has been built up since the module was first imported,
including all our work in progress.

We do not want to separate functions and the data they use into different
modules, since this would proliferate modules and also make the code 
more verbose by requiring the functions to qualify each data item
with its module name.

Our solution is to put each module's data definitions into a separate file
and code the module to execute that file's contents using Python *exec*, 
but only the *first* time the module is imported into the Python session.
In this way, the data can belong to the same module as the functions,
but reloading the module does not re-initialize the data.
For an example, see how the *sked* module conditionally *exec*'s the 
code in the file *skedinit.py*.

### No classes or objects ###

In Python, reloading a class into a running Python session is not
useful, because persistent objects continue to use the old class
definition.   Therefore, we do not write classes. (Classes built
into  Python itself, or in code written by others, are not a problem
because we do not reload them.)

This is not as serious a limitation as it might seem. Classes are not
really necessary because Python already provides a rich collection of
built-in compound data types which, by themselves or in combination, are
sufficient to support any activity. Then we can write ordinary functions
that act on these, instead of methods.

In particular, we use dictionaries instead of objects.  The 
dictionary keys act as attribute names and dictionary values
act as attribute values.   This has the advantage that new
attributes can be added at any time without requiring changes
to existing code and without invalidating any persistent data.
We use the dictionary *get* method to read dictionary items,
because this does not crash when an item is missing from old
persistent data; it just returns an appropriate default.
For examples, see the functions *save_buffer* and *restore_buffer*
in the *sked* module.

Revised Jun 2023
