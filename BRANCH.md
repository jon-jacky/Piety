
branches
========

This is the **parse_check** branch: separate *parse* and *check* modules
out of *ed*, other *ed* cleanup.

Branches recently merged into **master**:

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

Revised 23 Oct 2017
