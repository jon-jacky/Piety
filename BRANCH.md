
branches
========

This is the **args** branch: add arguments to the *Console* *__call__*
method that are analogous to command line arguments, so Piety console
jobs can be invoked in an interactive Python session with the same
names and same arguments that the corresponding standalone programs
are invoked from the system command line.  Revise the *startup* and
*main* functions in *ed*, *edsel* and other programs, to adopt a
uniform organization that works the same in both an interactive Python
session and a standalone program.  Rename each modules's *main*
function to the same name as the standalone program (the module name,
that is).  Revise or replace several instances of confusing or overly
complicated code: Replace the *ed.configure* function and the
variables it updated by a new *config* module.  Untangle *do_command*
in *ed* and *edsel*.  Simplify the *x* (script execution) command in
*edo* and *samysh*.  Make many minor revisions in style and naming.
Add some documentation *.md* files and revise others.  Begun 30 Jan
2018.

Branches recently merged into **master**:

- **nojob**, merged 28 Jan 2018.  Simplify and generalize job control.
Eliminate the *Job* class, absorb its functionality into *Session* and
*Console*.  Add *Job* Enum.  Eliminate the *InputLine* class, absorb its
functionality into *Console*.  Revise some modules in *scripts/*,
eliminate others.  Begun 2 Jan 2018.

- **parse_check**, merged 2 Jan 2018.  Separate *parse* and *check*
modules out of *ed*.  Remove unnecessary globals from *ed*.  Simplify
*ed* *do_command*.  In *Piety/test/ed*, revise and add *.ed* and
*.edo* scripts, revise and add reference *.log* and *.txt* files, add
*.sh* scripts for test automation.  Begun 6 Dec 2017.

- **modes**, merged 6 Dec 2017.  Simplify and generalize use of modes to
select prompts, keymaps, and handlers in *console*.  Add *wyshka*, a
new command line shell for console applications that provides modes
for application commands and Python statements.  Shorten and focus
*ed* by moving out code that supports test scripts to the new *samysh*
module that can execute a command with optional echo and delay.
Revise contents of *editors/* to use revised *console*, *wyshka*, and
*samysh*.  Begun 25 Oct 2017.

- **pysh**, merged 23 Oct 2017.  Revise *shell/pysh.py* to use the Python
standard library *code* module.  Begun 10 Oct 2017.

- **run_timestamps**, merged 10 Oct 2017.  Show timestamp tasks updating
windows concurrently with display editing in other windows.  Begun 14
Sep 2017.

- **resume**, merged 8 Sep 2017. *ed* and *edsel* revisions to restore
    session by calling *main()* after quit or crash.  Fix bugs in
    display updates.  Begun 14 Aug 2017.

- **frame**, merged 12 Aug 2017. Separate display and window
    management code out of *edsel* into new *frame* module.  New
    *frame* does not depend on *edsel*, *ed*, or any other
    application.  Applications communicate with *frame* using the new
    *update* and *updatecall* modules.  Begun 8 Mar 2017.

Revised 24 Mar 2018
