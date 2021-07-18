
branches
========

This is the *master* branch.  Branches recently merged into *master*:

- **noblock**.  Merged 18 Jul 2021.  Do not block after prefix characters
  like *C-x* while waiting for the next character.  Begun 5 Jul 2021.

- **metakey**.  Merged 3 Jul 2021. Support the *Meta* key modifier *M-*, often
  provided by the   *Alt* key on the keyboard.  Add Meta key display
  editing commands similar to   those in *readline* and *Emacs*: *M-b M-d
  M-f M-v M-< M-> M-q*

  Add the *Control-x* prefix *C-x* for display editing commands similar to
  *Emacs*: *C-x o C-x 1 C-x 2 C-x C-x*

  After receiving the *C-x* prefix, *edsel* blocks, waiting until the
  second character is received.   If *edsel* is running under the *Piety*
  scheduler, no other tasks can run during this interval.

  To invoke commands from display editing mode, use *M-x* like *Emacs*, no
  longer *C-x* which is now  a prefix.

  Add the *C-j* display editing command to execute the current line in the
  buffer with Python and append output to the end of the buffer.  This
  makes any buffer into  a Python REPL with a saved transcript.  

  *C-j* replaces *C-t* (*^T*) from Feb 2021 (below).  It only works on 
  the current line.  Neither *C-j* nor *T* advance the mark.

  Add the *edo* Z command and the *M-j* display editing command, to
  execute the current line with the system shell and append the output to
  the end of the buffer.

  *edsel* internals: use the *load_line()* and *store_line()* methods
  consistently to move text between the persistent text buffer and the
  line editing buffer.

  Bug fix: the paragraph fill *]J* command and *M-q* display editing command
  handle the last line of the buffer correctly.

  Revise *.md* and *.txt* files to explain new shell function and 
  new display editing commands with *M-* modifier and *C-x* prefix, etc.

  Begun 15 Feb 2021.

Recent work in the *master* branch:

- Feb 2021.  Add the *T* command to *edo*.   It executes the selected
  lines with with the Python interpreter, appends the output to the buffer,
  adds a new line after that and places *mark* and *dot* there. Subsequent
  typing advances dot but leaves mark, so all text typed after the last 
  Python output is in the selection region, ready to be executed by *]T*.
  The *edsel* *^T* command invokes *edo* *T* on the selected lines.
  These commands turn any buffer into a Python REPL.

  There are some inconveniences with *T*.  Error output still appears in the
  scrolling region, not the buffer.  Some Python output appears in very long
  lines that are not automatically wrapped.

  Oct 2020.  Rename *Piety/applications* directory to *samples*.

Branches recently merged into *master*:

- **bimport**.  Merged 26 Oct 2020. Add the the *bufimport* module 
  with functions to import or reload a module directly from a text buffer,
  without having to write it out to a file.  Add the *shellcmd* module
  with a function to run a system shell command.  Revise the *wyshka*
  module to use the  new *text* module instead of *ed*, completing the
  work of the previous two branches. Begun Oct 8 2020.

  When the *bimport* branch was merged, we finished the first stage of
  the Piety project.  We have provided all the features described in the
  [design document](doc/analogies.md).

- **textframe**.  Merged Oct 8 2020.
Rename the *storage* module to *text*.  This name
is analogous to *frame* for the display module -- it is not a generic
display, but a particular kind.  Also rename *frame_wrapper* to *textframe*,
to indicate it is where the *text* storage module and *frame* display module
are put together.  Also, fix bug from the previous *ed_frame* branch:
now display updates can be turned on and off during a Python session.
Begun Sep 30 2020.

- **ed_frame**.  Merged Sep 30 2020.
Remove display code from the *ed*, *storage*, and
*buffer* modules -- finally!  None of these modules imports the display
module *frame* anymore, and they no longer contain all those *if
displaying: ...* statements.  This simplifies those modules, and also
makes it possible to use them with a different display system. We provide
a new module *frame_wrapper* that wraps functions in *ed* and *storage* and
methods in *buffer* to call display code in *frame*.  We revise the
display editor *edda* (which is imported by  *edsel*) to import and use
this new *frame_wrapper* module. Begun Aug 7 2020.

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

Revised Jul 2021


