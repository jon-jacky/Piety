
Piety desktop
=============

Piety can provide a 'desktop' with a Python console, an
editor. a web browser, a terminal, and other Python
applications, all controlled by a custom window
manager in a single full-screen terminal.

<!-- ![Piety desktop](../screenshots/editor_sked_edsel_directory.png)

Use HTML (below) instead of this markdown to adjust size.
width=50% [works but width="960" does *not* work.
-->

<img src="../screenshots/desktop_startup.png"
 alt="Piety Desktop at startup" width=67% height=67%>

[Quick Start](#Quick-Start)  
[Appearance](#Appearance)   
[Workflow](#Workflow)  
[Commands](#Commands)   
[Keycodes](#Keycodes)   
[Other Instructions](#Other-Instructions)
[Files](#Files)   
[Influences](#Influences)

### Quick Start ###

There isn't any installation procedure. There are no
dependencies. Just clone the Piety repository under
your home directory:

    git clone  https://github.com/jon-jacky/Piety.git

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

    python3 -im desktop

The desktop appears, with the windows showing
the buffers named in a startup file (see
[Files](#Files)). 

If this is your first time using Piety, it will
be helpful to read and work through the interactive
tutorial displayed in the window on the right.

After you become familiar, you can run the desktop by typing
[commands](#Commands) at the Python prompt, or by typing
[keycodes](#Keycodes) in a window.

### Appearance ###

The Piety desktop contains an 80 column wide *editor
panel* on the left and a *viewer panel* that occupies
the remaining columns on the right, usually fewer than
80 if a comfortably large enough font size is chosen.
The editor panel can contain one or two windows, stacked
vetically.  The viewer panel can only contain one window. 

Below both panels is the Python *REPL region*. that extends the
full width of the display.

<img src="../screenshots/editor_sked_edsel_directory_sl.png"
 alt="Piety Desktop showing code and directory listing" width=67% height=67%>

 
### Workflow ###

The interactive Python interpreter runs in the REPL
region. Here you can type any Python statement. Some
statements are commands to start a Piety activity in a
window. (Piety has *activities* instead of
applications, as explained
[here](../editors/HOW.md).)

At all times, one window is the *focus window* which
displays a cursor where typed input appears. The
activity running in the focus window detects and
executes typed keycodes. Some commands typed in the
REPL start an activity in the focus window, or display
some output in the focus window. There are many
commands that select or change the focus window,
sometimes as a side-effect of something else, for
example listing a directory of files.
 
(When the REPL is selected, the cursor moves from the
focus window to the REPL region, and typed input
appears there. Meanwhile, the same window retains the
focus, and when the REPL operation is complete, the
cursor returns there.)
 
Any activity can run in any window, including editors.
You can edit in the viewer panel window just as you
can in the editor panel windows, except that window is
narrower.

Although the viewer window can support any activity,
it is intended to display information that informs or
supports activities in the editor windows: directory
listings, lists of editor buffers, shell commands and
their output, instructions and documentation
(including this very file -- note its short line
length). 

Some commands make special use of the viewer window,
to help make the workflow convenient. For example,
some commands, given while an editor window has
focus, display information in the viewer window --
such as a list of buffers or files -- without losing
focus from the editor window. Some commands given in
the viewer window, for example to select a file from a
list there, open the selected file in an editor
window. (This scenario is illustrated by the
screenshot above.)
 
### Commands ###

Here are commands (that is, function calls) you can
type in the Python REPL to use the desktop. To get to
the REPL from display editing mode, type *M-x* (*meta
x*, hold down the *alt* key while typing the *x* key).

A few of the commands here, and many others that work
in any window on the desktop, are also discussed in
the pages about the
[editors](../editors/README.md) and the
[browser](../browser/README.md).
 
Many of these commands are usually invoked in the
display editor, by pressing [keycodes](#Keycodes) (see
below), instead of typing commands in the REPL.

Session management:

- **ve()** - Switch from the REPL to display editing
    in the focus window.  *pm()* also works.

- **quit()** - Prompts *Are you SURE ...?* If the
    response starts with *y* or *Y*, exits the Piety
    session and returns to the host system prompt.

- **vwin()** - Create the viewer window to the right
    of the editor panel, if it does not already exist. Not
    needed if you start the Piety session from the *desktop*
    script, as described in *Quick Start* above.

- **vclr()** - Erase viewer window from the display,
    including border and status line. Needed only for
    testing the *vwin()* command.

Files and buffer contents:

- **e(fname)** - Load the file named *fname* into a
    buffer, and display it in the focus window. *fname*
    can include a relative or absolute path. Generate a
    buffer name *bname*, usually *fname* without any path
    prefix.
    If file *fname* does not exist, create a new empty buffer,
    whose contents can be written out to the file system later.

- **gr(url)** - Load the web page at *url* into *two*
    buffers: the HTML source, and the rendered text.
    Display the rendered text buffer in the focus window.

- **loader()** - Select a file or web page from the
    viewer window, load it into a buffer, and display it
    in the editor window.
    
- **b(bname)** - Display the buffer named *bname* in
    the focus window.

- **b()** - Switch back to the previously displayed
    buffer in the focus window. Repeating *b()* alternates
    between the current and previous buffer.

- **N()** - Show list of buffers in viewer window. The
    list is in a buffer named \*Buffers\* which is
    rewritten each time *N()* is invoked. Editor
    window keeps focus if it has it.
 
- **clear_buffers()** - Deletes all buffers except *scratch.txt*.
    First, prompts *Are you SURE ...?*

- **clear_webpages()** - Deletes all buffers whose file names
    begin with *http*.  First, prompts *Are you SURE ...?*

Navigating among windows:

- **ov()** - Switch focus from an editor window to the
    viewer window.

- **oe()** - Switch focus from the viewer window back
    to the editor window which most recently had focus.

- **o2()** - In a single editor window, split into two
    editor windows. The original window keeps the focus.
    Has no effect in the viewer window -- there is always
    only one.
      
- **on()** - In an editor window, when there are two
    editor windows, switch focus to the other editor
    window.
    
- **o1()** - In an editor window, when there are two
    editor windows, delete the other editor window.

Navigating within windows:

- **v()** - Scroll down (forward) in focus window.

- **rv()** - Scroll up (back) in focus window.

- **top()** - Go to top of buffer in focus window. 

- **bottom()** - Go to bottom of buffer in focus window.  

- **vv()** - Scroll viewer window down.  Editor window 
    keeps focus if it has it.

- **vrv()** - Scroll viewer window up. Editor window keeps
    focus if it has it.

- **vtop()** - Go to top of buffer in viewer window. 
    Editor window keeps focus if it has it.

- **vbottom()** - Go to bottom of buffer in viewer window.
    Editor window keeps focus if it has it.

- **vrefresh()** - Redraw the viewer window on the
    display, including its border and buffer contents.
    Needed only if viewer window becomes corrupted.

- **vvrefresh()** - Redraw viewer window.  Editor window
    keeps focus if it has it.

Viewer window contents:            

- **sh(cmd)** - Run a shell command in the viewer window.   
    Execute *cmd*, a shell command string,
    in a shell subprocess. Echo the command and write the
    command output at the end of the \*Console\* buffer.
    Display the \*Console\* buffer in the viewer window.
    The editor window keeps the focus, if it already has it.
    
- **cd(path)** - Change current working directory to
    *path*, a string.    
    Echo command (which shows the
    *path*) at the end of the \*Console\* buffer.
    Display the \*Console\* buffer in the viewer
    window. The editor window keeps the focus, if it
    already has it.

- **pwd()** - Show the current directory in the viewer
    window.    
    Print the current working directory the
    end of the \*Console\* buffer. Display the
    \*Console\* buffer in the viewer window. The
    editor window keeps the focus, if it already has
    it.

- **ls(path)** - Show a compact directory listing
    in the viewer window.   
    Execute the *ls path* command in a 
    a shell subprocess to show a compact directory 
    listing.. Default *path* is the current working
    directory. Echo the command (which shows the
    *path*) and the directory listing at the end of
    the \*Console\* buffer. Display the \*Console\*
    buffer in the viewer window. The editor window
    keeps the focus, if it already has it.

- **lsl(path)** - Show a long directory listing
    in the viewer window.   
    Execute the *ls -l path* command in a 
    a shell subprocess to show a long directory
    listing with one line per file. Default *path* is
    the current working directory. Echo the command
    (which shows the *path*) and the directory listing
    at the end of the \*Console\* buffer. Prefix each
    file name in the listing by the *path* (unlike the
    shell *ls -l* command), so it can work with the
    *loader* command (above). Display the \*Console\*
    buffer in the viewer window. The editor window
    keeps the focus, if it already has it.

- **lslt(path)** - Show a long directory listing 
    sorted by date in the viewer window.    
    Execute the *ls -lt path* command in a 
    a shell subprocess to show a long directory
    listing with one line per file, sorted by 
    time, with the most recent files first. Default
    *path* is the current working directory. Echo the
    command (which shows the *path*) and the directory
    listing at the end of the \*Console\* buffer.
    Prefix each file name in the listing by the *path*
    (unlike the shell *ls -lr* command) so it can
    work with the *loader* command (above). Display the
    \*Console\* buffer in the viewer window. The
    editor window keeps the focus, if it already has
    it.

- **man(topic)** - Show a manual page in the viewer 
    window.   
    Execute the *man topic* command 
    in a shell subprocess to print the manual page
    on *topic*, a string.  Create a new buffer named
    *topic.man* to hold the manual page and display
    it in the viewer window.  The manual page is 
    formatted to fit in the viewer window. The editor
    window keeps the focus, if it already has it.

- **help(topic)** - Show Python help in the viewer
    window.   
    Execute the Python *help(topic)*
    command to print information about *topic*, a 
    Python object.  Create a new buffer named
    *topic.help* to hold the help text and display
    it in the viewer window.   The help text is
    not formatted to fit in the viewer window, but
    you can use editor commands to wrap long lines.
    The editor window keeps the focus if it already
    has it.

- **loader(this_window)** - Select the item on the current line
    in the viewer window.  The item might be a buffer, file or directory.
    If *this_window == True*, display the item in the viewer window.
    If *this_window == False*, display the item in the editor window
    (except directories, which are always displayed in the viewer window)
            
### Keycodes ###

Keycodes you can type to invoke desktop
[commands](#Commands) (above) while in display editing
mode. To get to display editing mode from the Python
prompt in the REPL, type the function call *ve()*
(*pm()* also works).

Here *C-x*, *control-X*, means hold down the *ctrl*
key while you type the *X* key. *M-x*, *meta-X*, means
hold down the *alt* key while you type the *X* key.

Many (but not all) of our keycodes are the same as the 
[Emacs keycodes](https://www.gnu.org/software/emacs/refcards/pdf/survival.pdf)
used by the Emacs editor.

Session management: 

- **M-x** - Exit display editing and return to the
    the Python command line. To return to display
    editing again, type the command *ve()*.
    *pm()* also works.
    
- **M-y** - Type just one command at the Python
    prompt, then return immediately to display editing,
    without having to type *pm()*.

- **C-x 3** - Create viewer panel.  Not needed if session
    was started from the *desktop* script.

- **C-x 1** - Delete viewer panel, if viewer panel has
    focus.   Needed only for testing *C-x 3*.

Files, directories, and buffers:

- **C-x C-b** - Show list of buffers in viewer window.

- **C-x b** - Show named buffer in focus window, enter buffer
    name at prompt.   Type RET for the default, return to previous buffer.
  
- **C-x C-d** - List file directory in viewer window.  Enter 
   relative or absolute directory path at prompt.  Type RET for the default,
   the current working directory.

- **C-x C-f** - Load named file into focus window, enter file
    name at prompt.  If there is no such file, create a new empty buffer,
    whose contents can be written out to the file system later.
    There is no default, type RET to cancel the operation.

- **C-o** and **M-o**  - Select the item on the current line in the list
    in the viewer window.  The item might be a buffer, file or directory.
    Type *C-o* to display the item in the viewer window.
    Type *M-o* ti display the item in the editor window
    (except directories, which are always displayed in the viewer window)
            
Navigating among windows:

- **C-x v** - Switch focus from editor window to viewer window.

- **C-x e** - Switch focus from viewer window back to most recent 
    editor window.

- **C-x 2** - Split editor window in two.  No effect in viewer 
    window.
    
-  **C-x 1** - Return to single editor window by deleting 
    editor focus window.  Delete viewer window if it has focus.

- **C-x o** - Switch focus to other editor window, 
    if there is one.

Navigating within windows:
    
- **C-v** - Scroll down (forward) in focus window.

- **M-v** - Scroll up (back) in focus window.

- **M-<** - Go to top (beginning) of buffer in focus
    window.

- **M->** - Go to bottom (end) of buffer in focus
    window.

- **C-t** - Scroll down in viewer window.
    Editor window keeps focus if it has it.

- **M-t** - Scroll up in viewer window.
    Editor window keeps focus if it has it.

- **M-(** - Go to top of buffer in viewer window.
   Editor window keeps focus if it has it.

- **M-)** - Go to bottom of buffer in viewer window.
   Editor window keeps focus if it has it.

- **C-x l** - Refresh focus window, an editor or viewer window.

- **M-m** - Refresh viewer window while editor window has focus.


### Other Instructions ###

Other instructions for using the desktop appear in the files
*viewer/desktop.txt* and *viewer/keys.txt*.   These files are usually
loaded into the Piety session at startup.

### Files ###

These files are in the *Piety/viewer* directory:

- **README.md**: This file.

- **desktop.txt**: Interactive tutorial on using the desktop,
    formatted for display in the viewer window.
 
- **keys.txt**: List of keys and key sequences used for navigating
      the desktop and editing text in its windows, formatted for
      display in the viewer window.
  
- **viewer.py**: Source code for the viewer window, including the
    keys and commands.

- **desktop.py**: Script to start a Piety desktop session.

- **desktop_startup.py**:  Script to configure the Piety desktop
    at startup, called by *desktop.py*.
    
### Influences ###

The Piety desktop is influenced by 
[Emacs](https://www.gnu.org/software/emacs/tour/index.html),
[Oberon](https://people.inf.ethz.ch/wirth/ProjectOberon/UsingOberon.pdf), 
and [Acme](http://acme.cat-v.org/).

Revised May 2026

