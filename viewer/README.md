
Piety desktop
=============

Piety can provide a 'desktop' with a Python console, an
editor. a web browser, a terminal, and other Python
applications, all controlled by a custom window
manager in a single full-screen terminal.

<!-- ![Piety desktop](../screenshots/editor_sked_edsel_directory.png)

Use HTML (below) instead of this markdown to adjust size.
width=50% [Aworks but width="960" does *not* work.
-->

<img src="../screenshots/editor_sked_edsel_directory_sl.png"
 alt="Piety Desktop" width=67% height=67%>

[Quick Start](#Quick-Start)  
[Appearance](#Appearance)   
[Workflow](#Workflow)
[Commands](#Commands)   
[Keycodes](#Keycodes)   
[Influences](#Influences)

### Quick Start ###

There isn't any installation procedure. There are no
dependencies. Just clone the Piety repository under
your home directory.

Run this command to put the Piety modules on your
*PYTHONPATH*, so you can run them from any directory.
Note the dot at the beginning of the command:

    . ~/Piety/bin/paths      

The Piety desktop can run in a terminal window
expanded to full screen in a graphical desktop, or in
a full screen text-only console.

Select a font size that can display at least 135
columns across the full width of the display.

Run this command to start the desktop:

    python3 -im pmf

Now you can run the desktop by typing
[commands](#Commands) at the Python prompt, or by
typing [keycodes](#Keycodes). (All keycodes invoke a
command, so we just say 'commands' for 'commands and
keycodes'.)

### Appearance ###

The Piety desktop contains an 80 column wide *editor
panel* on the left and a *viewer panel* that occupies
the remaining columns on the right, usually fewer than
80 if a comfortably large enough font size is chosen.
The editor panel can contain one or two windows. The
viewer panel can only contain one window. 

Below both panels is the *REPL region*. that extends the
full width of the display.
 
### Workflow ###

The interactive Python interpreter runs in the REPL
region. Here you can type any Python statement. Some
statements are commands to start a Piety activity in a
window. (Piety has *activities* instead of
applications, as explained
[here](../editors/HOW.md)

At all times, one window is the *focus window* which
displays a cursor where typed input appears. The
activity running in the focus window detects and
executes typed keycodes. Some commands typed in the
REPL start an activity in the focus window, or display
some output in the focus window. There are many
commands that select or change the focus window,
sometimes as a side-effect of something else, like
selecting an editing buffer.
 
(When the REPL is selected, the cursor moves from the
focus window to the REPL region, and typed input
appears there. Meanwhile, the same window retains the
focus, and when the REPL operation is complete, the
cursor returns there.)
 
Any activity can run in any window, including editors.
You can edit in the viewer panel window just as you
can in the editor panel windows, except that window is
narrower.

The viewer window is intended to display information
that informs or supports activities in the editor
windows: directory listings, lists of editor buffers,
shell commands and their output, instructions and
documentation (including this very file -- note its
short line length). Some commands make special use of
the viewer window, to make the workflow convenient.

For example .... (explain lsl() then loader())
(we need a better name than loader)
 
### Commands ###

### Keycodes ###

### Influences ###

The Piety desktop is  influenced by [Emacs](...?),
[Oberon](...?), and [Acme](...?).


Revised Jul 2025 
