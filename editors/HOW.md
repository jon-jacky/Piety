
How we program 
==============

We have all of our source code, our editors, and
the interactive Python interpreter always available in our
Python session.
We write code that we load and run immediately, without restarting
the session or losing any work in progress.

Our editors here -- [*sked*, *edsel*, *dmacs*, and *pmacs*](README.md) --
were developed in this way.  The first two hundred
lines of *sked* were written in another editor and
then imported into an interactive Python session. 
After that, *sked* was developed incrementally
in the long running session.  We used the rudimentary *sked*
to edit its own source code, adding functions one or two 
at a time, then reloading the module into the same session,
using the new functions right away on the same source files.
Proceeding in the same way, we used *sked* to write *edsel*, 
*edsel* to write *dmacs*, and *dmacs* to write *pmacs*.

To make this possible, we had to adopt a Python coding style
that has some unusual features.  The small collection of modules
here that we have written in this style comprise a Python programming 
environment which is minimal, even crude.  But we find
that its malleability and responsiveness
motivate us to continue working in it, despite its lack of conveniences.

The following sections describe some features of our programming style.

### Long-running session ###

We do not write "applications".  An application is software dedicated to
a single activity.  It runs by itself in its own short-lived 
Python session.  It loads a fixed set of functions and data that are
isolated from other applications, that disappear when the application exits.
In contrast, we work in a long-running Python session, where we build an
ever-growing collection of functions and data that persist and
support many activities, where all are potentially accessible to any others,
and are always available for ad-hoc experiments at the REPL.

The function calls  are transient, although the data they create can persist.
The function calls might take over the keyboard and screen for a while, but
the Python interpreter is often visible in part of  the screen, and is always
accessible with a keystroke or two.

We don't invent command languages or write command interpreters; 
we use Python for that.  The Python interpreter itself is the "main
program" that invokes the functions in our modules.

### Reloading modules ###

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

Our solution was to put a *try ... except ...* block at the beginning
of each module.   The *try* block contains a single statement that 
reads one of the variables in the module.  This statement succeeds
every time the module is reloaded, but it fails the first time the
module is imported.  Only that one time, the *except* block is executed.
It initializes all the module-level variables in the module -- just that once.
After that, the module can be reloaded any number of times without
re-initializing any module-level variables.
For example, see the *try ... except ...* block at the beginning 
of the *sked* module.
 
### Modules and dictionaries instead of classes and objects ###

Reloading a class into a running Python session is not
useful, because persistent objects continue to use the old class
definition.   Therefore, we do not write classes. (Classes built
into  Python itself, or in code written by others, are not a problem
because we do not reload them.)

Instead, we program with modules and dictionaries, which do acquire
the new behaviors when modules are reloaded.

An ordinary Python module resembles a class definition.   The module-level
global variables are like attributes (instance variables) and the functions in
the module are like methods A module also resembles one object - a single
instance of the data defined by the module.  You can have many objects of the
same class in  the Python session at the same time, but you can only have one
instance  of a module. We use modules instead of classes where *we only need
one instance  to be active at a time*.

For example, our *sked* module defines the data and functions used by a text
buffer in our editors.  The  editors can work with multiple buffers, but only
one of the buffers is active at a time.  You can only insert text into one
buffer at a time -- and so on.   Typically, you edit in the same *current
buffer* for a while and then select another buffer to be the current buffer,
then edit in that buffer, etc.

The state of the current buffer is stored in the module-level global
variables of the *sked* module.  These variables are  updated by almost
every editing command -- by every keystroke in  the *dmacs* and *pmacs*
editors.

The states of all the other buffers  are stored in dictionaries.  For
each buffer, there is a dictionary.  The keys in this dictionary are the
names of the variables in the *sked* module, and the values in this
dictionary are the variable values.    When a new current buffer is
selected, the variables of the previous current buffer are saved in its
dictionary, and the variables in the new current buffer are restored
from its dictionary.   See the functions *save_buffer* and
*restore_buffer* in the *sked* module.

The whole persistent collection of saved buffers is stored in a
dictionary whose keys are the buffer names, and whose values are the
dictionaries for each buffer.   It is a dictionary of dictionaries,
*buffers* in the *sked* module.

When we add or delete variables from the buffer module *sked*, we make
corresponding changes to to the code that saves and restores the
variables in the dictionaries.   This does not invalidate the persistent
data in the saved dictionaries. When we restore module variables from a
dictionary,  we use the *get* method to read dictionary items, because
this does not crash when an item is missing from old persistent data; it
just returns an appropriate default.

An alternative to saving and restoring module global variables from
the dictionaries would be to pass the appropriate dictionary to 
each function as its first argument.  This would be quite like the
*self* argument in Python methods.  We rejected this alternative because
it would make the code more verbose.


## Brevity: short function names, default arguments, global variables ###

We often work at the Python REPL, so we try to make this as easy as
possible.  We try to minimize typing effort. To achieve
this, we sometimes employ programming practices that are usually
considered poor style.

At the Python REPL, commands are function calls.  So we use short function
names.  The names of the functions in the *sked* editor that are editing
commands are just single characters.  We use the same single-character 
command names in *sked* as are used in the classic Unix editor *ed*.

To further shorten function calls, we minimize the need to type function
arguments by providing optional arguments with helpful default values.

The helpful defaults are  context-dependent, so they can't be hard-coded
in the function definitions. Instead, we code each optional argument in
the form *arg=None*, so it can be omitted in function calls.  The body
of the function contains a  statement of the form *if not arg: arg =
default*  where *default* is a global variable that is updated while the
program executes, to provide the most helpful default value at each time.
If that argument is omitted from the function call, the default 
argument is used.  Or, you may provide a value for the argument to 
use instead of the default.

For example, the default for the location where text is inserted,
deleted, or changed, is updated by each editing operation to be the
location where the most recent change was made.  The default text string
to search for or replace is the same string as was last searched for or 
replaced.  The default buffer to change to is the buffer that was most
recently visited.

To eliminate more function arguments, function bodies use global
variables instead.   This works perfectly well when the same global 
variable is always used by the function, so there is no need to pass 
an argument.  We also use a global variable where the same variable value
is used for many consecutive function calls.  In that case it is easier
to reassign the global variable from time to time, than it is to pass an
argument to every function call.   The variable *buffer* in the *sked*
module is an example.

Revised Jan 2024

