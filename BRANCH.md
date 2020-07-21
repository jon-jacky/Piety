
branches
========

This is the **master** branch.  Branches recently merged into *master*:

- **storage**, merged Jul 21 2020.  Separate buffer data structures out of
*ed.py* into  the new *storage* module.  Add *noed* ("no ed"), an editor
with storage and display but no commands or any user interface except the
interactive Python interpreter.  Begun Jul 1 2020.

- **paragraph**, merged Jun 30 2020.   Add functionality and reorganize
code in editors. Add new paragraph address range *]* to *ed.py*, sometimes
more convenient than selecting a region with mark. Revise *J* *wrap*
command to properly re- wrap already-indented text. Support regular
expressions in line address patterns and the *s* substitute command. Print
*? no match* when the search pattern is not found in the buffer, or the
replacement pattern is not found in the line.   Support classic *ed*
default empty pattern in *s* command: *s//new*.   Add classic ed *u*
command, undo previous substitution. Reorganize search and line address
code in *buffer.py* *ed.py* *buffer.py* *check.py*. Print *? no mark* from
*edsel* *^Q* and *^W* commands.  Ensure that text deleted, altered, or
copied by  *ed* *y* *d* *c* *s* commands can be restored by *edsel* *^Y*
as well as *ed* *x*. Add and revise documentation in several *.md* and
*.txt* files. Begun 26 Apr 2020.

- **flatten**, merged 25 Apr 2020.  Simplify the display update modules 
*frame* and *window*, improve their organization
and style, and make corresponding revisions in their clients *buffer*, *ed*, 
*edda*, and *edsel*.  In *frame*,  replace its large  *update* function 
with each of its many nested cases  turned into a  separate small 
function, whose name is the same as the *Op*  *Enum* value that was used 
to select that case.  Each function has just  the  minimum of positional 
arguments it needs,  instead of many optional  keyword  arguments.  Remove 
the *updates* module with its *Op* enum; they  are no longer needed to 
select cases.  Remove the *view* module with its  no-op *update* function 
that suppresses output when no display.  Instead, in *ed* and *buffer* 
have a boolean variable *displaying* that explicitly guards *import frame* 
and each call to a *frame* display function.  In *window*, simplify code 
and  remove redundancies, rename several methods, reorder methods in the 
file.  Revise  explanations in *frame.md* and *window.md*, minor revisions 
to other *md* files.  Bug fixes in *ed.py* and a few other modules.  Bring some
tests in *test/edda* up to date.  Begun 17 Jan 2020.

- **redirect**, merged 13 Jan 2020.  Provide redirection of command output
*stdout* to text buffers (instead of the scrolling command region) in the
*wyshka* shell. Revise commands in *edo* (and *edsel* etc.) for running
code from text buffers, begun in *runlines* branch: *R* runs code using
*eval*, *P* runs code using interactive interpreter *push*. Add commands
to *ed* (and *edsel* etc.): indent *I* and outdent *O*,  wrap lines *J*,
and list buffers to the buffer named *Buffer* *N*. Add new *ed* address
range abbreviation *[*, the lines in the region from the mark to dot
(which is usually selected in *edsel*). Begun 6 Jul 2019.

- **runlines**, merged 4 Jul 2019.  Execute the current selection
(from mark to dot) with the Python interpreter, in display editing mode with
a keystroke.  For obscure reasons, the code for executing Python lines from a
buffer in command mode, added in the *edsel* branch (below), does not work for
this.  Also, a few more style tweaks as in *edsel_cleanup* (below).
Begun 30 May 2019.

- **edsel_cleanup**, merged 29 May 2019.  Tweak naming and style in
*ed*, *buffer*, *console*, *edsel*, *frame*, *window*, and *display*.
Break dependence of *edsel* (formerly *eden*) on *display*, now only depends
on *frame*. Begun 23 May 2019.

- **xcommand**, merged 21 May 2019.  Extract *params* function from *edo* *X_command*,
move to *samysh* module.   Change *echo* parameter in *samysh* *show_command* and *run_script*
from lambda to simple boolean.  Begun 21 May 2019.

- **edsel**, merged 20 May 2019.  Rename these editors: *edda* to *edna*, *edsel* to *edda*,
*eden* to *edsel*.   Reserve the name *eden* for a program we may add in the future.
We rename these files and replace these pervasive names in the many files
where they appear by running Python scripts, without resorting to
the shell, *sed*, or any other utilities outside Piety.  To make this self-contained,
we add editor commands to run Python scripts from editor buffers and selections.
Begun 10 May 2019.

- **eden**, merged 9 May 2019.  Add full screen editing to the *eden*
display editor, in addition to the classic *ed* *insert* and *append*
commands.  Make *eden*, including its built-in Python shell, into a
minimal but self-contained Python programming environment.  Also,
improvements to usability, organization, style and documentation.
Rename each module's main function back to *main*, also rename the
*Console* *call* function to *main* so standalone programs and console
jobs can be started in Python with the same syntax: *ed.main()* etc.
Begun 1 Apr 2018.

- **noframe**, merged 1 Apr 2018.  Reorganize and simplify
communication between applications and display.  Break dependence of
*edsel* on *display*, now only depends on *frame*.  Several related
revisions.  Begun 26 Mar 2018.

- **args**, merged 24 Mar 2018.  Improvements to usability,
organization, style, and documentation.  Add arguments to the
*Console* *__call__* method that are analogous to command line
arguments, so Piety console jobs can be invoked in an interactive
Python session with the same names and same arguments that the
corresponding standalone programs are invoked from the system command
line.  Revise the *startup* and *main* functions in *ed*, *edsel* and
other programs, to adopt a uniform organization that works the same in
both an interactive Python session and a standalone program.  Rename
each modules's *main* function to the same name as the standalone
program (the module name, that is).  Revise or replace several
instances of confusing or overly complicated code: Replace the
*ed.configure* function and the variables it updated by a new *config*
module.  Untangle *do_command* in *ed* and *edsel*.  Simplify the *x*
(script execution) command in *edo* and *samysh*.  Make many minor
revisions in style and naming.  Add some documentation *.md* files and
revise others.  Begun 30 Jan 2018.

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

Revised Jul 2020

