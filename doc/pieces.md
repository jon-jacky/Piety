
Putting the Pieces Together in Piety
====================================

The Piety system is not just a single big program or an ad-hoc
collection of modules.  It is a collection of operating system
components and applications that can be put together systematically
into different configurations.  In this document we describe the
Python coding techniques we use to build up a Piety configuration from
independent parts.  We describe how the OS components and applications
are combined, and how they communicate with each other.

(The following are just rough notes and placeholders)

- In Piety, all operating system and application code runs in a single
Python session so any object might access (read and/or update) any
other object just by naming it (possibly through a long dotted path of
module and object names etc.).  This can be convenient, but it is
necessary to use care to ensure that the OS components remain
separable and able to be used in different combinations, and to ensure
that applications remain separable from the OS, so they can run
standalone (without Piety).

1. Changing configurations by changing PYTHONPATH, so that modules
with the same names, but from different directories, are used.
Explained in detail [here](modules.md).

2. Avoid dependencies (imports) by passing parameters instead.  Of
course this is an obvious and age-old technique.  We use it in several
ways, see 3 and 4 below.

3. Message passing.  Used to decouple window manager and window
updates from applications.  The window manager modulem frame, does not
depend on (import) applications (editors etc.), and vice versa.
Instead both frame and applications depend on (import) the small
message-passing updates module.  Here passing messages from
application to display is implemented by passing parameters to the
update() fcn.  Passing messages back to application is implemented by
update() return values.  update module imports frame BUT applications
only import update.  So we could write different update modules that
import different window managers (other than frame) and then use the
PYTHONPATH technique to select an update module for the window manager
in our chosen configuration.

4. "Wrapper" organization of Console job - wraps an application,
application handler and startup/cleanup fcns are passed to Console
__init__.  Also Piety job control fcns are passed to Console __init__.
Console collects input without blocking, calls handler fcn from app,
also connects application to Piety job control.

4. a. Use of "thunks" (callables, usually lambda exprs.) as parameters
in Console __init__ and maybe elsewhere, to reference variables in
other components.  IN this way, connections to different objects or
modules can be passed as parameters (instead of being hard-coded).
Passing a thunk rather than just the variable allows code to evaluate
the thunk to obtain the current (possibly different) value of the
variable each time code is executed, instead of always using the
(initial) value the variable had when __init__ was executed.  I
recall we also use this to handle prompt in pysh/wyshka/samysh and
maybe elsewhere.

5. "Onion" organization of editors - each editor (layer of the onion)
imports the next simpler editor (next inner layer of the onion), then
its own do_command adds a few cases for new commands then control
falls through to call next inner editor's do_command.  I recall
shells wyshka > pysh use a variant of this technique also.  Or was
that just in samysh x (echo/delay) command?

5. a. Monkey patching (vocab?): outer layers of "onion" can add/change
functionality of inner layers in "onion" by reassigning functions and
variables.  For example edsel calls ed.configure to reassign ed's
do_command and update.

6. Are there other techniques in pysh/wyshka/samysh shells and their 
use in edo/edda than 1 - 4a above?

Revised February 2018