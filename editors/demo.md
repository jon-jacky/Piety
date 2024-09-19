
Adding and using a new editor feature: autoindent
=================================================

This page shows you how to add a new feature to the Piety *pmacs* editor.

Follow along with the instructions here to use the *pmacs* editor to edit
itself to add a new *autoindent* feature, then reload the revised code
into the same editing session, and then use the new feature to edit -- all
without restarting the editor session or losing any work that might be in
progress in other editor buffers.

The entire editor was built up in the same way as demonstrated here, adding
one feature at a time to a long-running editor session.

There are no "plugins" or "extension language" or any other special features
for editor  customization. All features are added by editing right in the
editor's own Python code.

These instructions assume you are already familiar with how to use the
*pmacs* editor. If not, read *Piety/editors/README.md*.
 
### The autoindent feature ###

In this demonstration we add an *autoindent* feature to the editor.

This feature makes it easier to type blocks of indented text, which occur
everywhere in Python source code.  Indented blocks also occur frequently in
markdown files, to indicate code samples, or entries in lists.

Autoindent affects the behavior of the ENTER (or RETURN) key.   Typing ENTER
opens a new line after the current line.   In the typical case where the
cursor is already at the end of the current line, typing ENTER opens a new
empty line.  Otherwise, it splits the line at the cursor and moves the text
after the cursor (called the suffix) to the new line.

Without the autoindent feature, typing ENTER always puts the cursor on the new
line in the first column, at the left edge of the of the window. Any suffix
text is aligned at the left edge also.  If that line should be indented, you
have to type several spaces to move the cursor (and any suffix text) to the
correct indented column.   You have to type the spaces at the beginning of
every line in the indented block.   It can be quite tedious. (In pmacs,
typing the TAB key once inserts several spaces).

With the autoindent feature, typing ENTER puts the cursor on the new line
at the proper indented column, lined up with the first nonblank character
in the preceding line.  So you can type a block of indented code more easily.
You still have to type (or delete) some spaces to indent the first line in each
block, but within the block, typing ENTER automatically starts a new line and
places the cursor at the indented column.

There is no way to turn off the autoindent feature, because this is not
necessary.  Simply type a line that begins in the first column, at the left
edge of the window.  Then typing ENTER will put the cursor in that first
column in all of the following lines, just as before.

### Find the code to revise ###

We want to change the behavior of the ENTER (or RETURN) key.  

First, we must find the code to revise.  We search the Piety source code
files for 'enter' and 'return'.   In *vt_terminal/key.py* we find the return
key is assigned the name *cr* (for "carriage return"). Searching the editor
source modules for *key.cr*, we find in the  *pmacs* module the *keymap*
table that associates *key.cr* with the *open_line* function -- so typing
the ENTER key calls *open_line*. That function determines the ENTER key
behavior, so that is function we will edit.
 
### Prepare files for the demonstration ###

In this demonstration, you will edit two files.  You will edit the editor
source code in *pmacs.py*, and edit some sample code in *sked_fragments.py*
(which contains code fragments from *sked.py*).

The current version of *pmacs.py* in the repository  already contains the
autoindent feature, and may contain more recent revisions as well.  To avoid
corrupting the current version of *pmacs.py*, and also to make the demo
reproducible so you can do it more than once, we provide the initial
version, and also  *sked_fragments.py* in the *editors/demo/* subdirectory.

To prepare for the demo, retrieve the initial versions of both files. 

The initial version of *pmacs.py* is named *pmacs_no_autoident.py.* Copy and
rename it from the *demo* subdirectory over *pmacs.py* in the *editors*
directory.   With *Piety/editors* as you default directory, use this command
on Unix-like systems:

    cp demo/pmacs_no_autoindent.py ./pmacs.py
    
Now your *pmacs.py* does not include the autoindent feature.  
We will restore the current version of *pmacs.py* after we run
the demo.

Copy *sked_fragments.py* from the subdirectory.  It is not necessary to rename it:

    cp demo/sked_fragments.py .
    
You must include that final dot.  Now you can try some editing.

### Demonstrate editing without autoindent ###

Start a new *pmacs* editor session, to ensure it will use the version 
without the autoindent feature that you just copied from the *demo* directory.

Load the file *sked_fragments.py* into the editor: the initial version you just
copied from *editors/demo* into *editors*.

In the *sked_fragments.py* buffer, scroll down a bit to the *try: ...
except: ...* block, which is at one level of indentation.

Put the cursor at the end of the last comment line in the *except* block.
Type ENTER (or RETURN).   The cursor appears on the next line, at the 
first column at the left edge of the window.  Type four spaces (or one TAB)
to indent the cursor under the preceding line.
Now type some code, for example these lines from the *except* block in
*sked.py*:

    dot = 0
    point = 0
    filename = 'scratch.txt'

At the end of each line, type ENTER (or RETURN).  Each time, the cursor 
goes to the first column, and you have to type spaces or tab to indent 
each line.

Next, scroll down to the *def w(...)* function definition.  Scroll down to
*if filename ...*, where there is a block with three levels of indentation.
Put the cursor at the end of the last line, then type ENTER (or RETURN).  The
cursor appears on the next line, in the first column at the left edge of
the window.  You have to type 12 spaces (or 3 tabs) to indent correctly.
Now type some code, for example this line from the triply-indented block
in the *w* function in *sked.py*:

    bufname = bname(filename)
    
### Edit the code ###  

Load the file *pmacs.py* into the editor: the initial version you just
copied from *editors/demo* into *editors*.

In *pmacs.py*, we find the *open_line* function:

    def open_line(keycode):
        """
        Split line at point, replace line in buffer at dot
        with its prefix, append suffix after line at dot.
        """
        suffix = ed.buffer[ed.dot][ed.point:] # including final \n
        ed.buffer[ed.dot] = ed.buffer[ed.dot][:ed.point] + '\n' # keep prefix on dot
        display.kill_line() # erase suffix from dot
        ed.buffer[ed.dot+1:ed.dot+1] = [ suffix ] # insert suffix line after dot
        ed.point = 0 # start of new suffix line
        ed.dot += 1
        if edsel.in_window(ed.dot):
            edsel.update_below(ed.dot)
        else:
            edsel.recenter()
        restore_cursor_to_window()

Here the text buffer is *ed.buffer*, a list of lines (which are strings),
and *ed.dot* is the index of *dot*, the current line in the buffer, so
*ed.buffer[ed.dot]* is the current line.  Here *ed.point* is the index of
the character under the cursor in the current line.

The line we are looking for here has the comment *# insert suffix line ...*.
We want to  change it to something like:

        ed.buffer[ed.dot+1:ed.dot+1] = [ <extra spaces> + suffix ]
                 
where *extra spaces* is a string of space characters of the proper length
to make the new line up with the current line. So we need to count the
spaces at the beginning of the current line, *ed.buffer[ed.dot]*.  Add
these two lines right before the *insert suffix ...* line

    nspaces = 0
    while ed.buffer[ed.dot][nspaces] == ' ': nspaces += 1
    
When the *while* loop exits, *nspaces* is the number of leading spaces in the
current line.  

Now change the *insert suffix ...* line to this:

        ed.buffer[ed.dot+1:ed.dot+1] = [ nspaces*' ' + suffix ] # indent by nspaces

There is one more detail.  We must put the cursor after the leading spaces.
Change the next line from this:

        ed.point = 0  # start of new suffix line

to this:

        ed.point = nspaces  # indent cursor
    
Here is the revised function.  We have added to the initial comment block, too:

    def open_line(keycode):
        """
        Split line at point, replace line in buffer at dot
        with its prefix, append suffix after line at dot.
        Preserve indentation: add as many spaces as needed before suffix line
         to match indentation of prefix line.
        """
        suffix = ed.buffer[ed.dot][ed.point:] # including final \n
        ed.buffer[ed.dot] = ed.buffer[ed.dot][:ed.point] + '\n' # keep prefix on dot
        display.kill_line() # erase suffix from dot
        # Auto-indent suffix line to same indentation as prefix line.
        nspaces = 0
        while ed.buffer[ed.dot][nspaces] == ' ': nspaces += 1 # count leading spaces
        ed.buffer[ed.dot+1:ed.dot+1] = [ nspaces*' ' + suffix ] # indent by nspaces
        ed.point = nspaces # indent cursor
        ed.dot += 1
        if edsel.in_window(ed.dot):
            edsel.update_below(ed.dot)
        else:
            edsel.recenter()
        restore_cursor_to_window()
    
### Reload the code ###

Now you are ready to save the edited *pmacs* module in the file system,
and reload it into the Python session.

Type the key sequence to command *pmacs* to write out the buffer and reload
its file into the Python session : *C-x C-r*.  Hold the CTRL key down while
you type the *x* key, then continue to hold the CTRL key down while you type
the *r* key.

These messages appear in the the scrolling REPL region at the bottom of the
window:

    Wrote pmacs.py, 273 lines
    Reload module pmacs

Now the revised *open_line* function including the autoindent feature is
loaded into the Python session.
 
### Demonstrate editing with autoindent ###

Now you can edit with the autoindent feature.

Return to the *sked_fragments.py* buffer and scroll down past the line
of ######.... to the *try: ... except: ...* block, which is at one level
of indentation.

Put the cursor at the end of the last comment line in the *except* block.
Type ENTER (or RETURN).   The cursor appears on the next line, indented 
under the first nonblank character in the comment line.  Now type some
code, for example these lines from the *except* block in *sked.py*:

    dot = 0
    point = 0
    filename = 'scratch.txt'

At the end of each line, type ENTER (or RETURN).  The cursor appears on the
next line, indented under the previous line of code.

Next, scroll down to the *def w(...)* function definition.  Scroll down a
bit  further to  *if filename ...*.  Under that there is a block with three
levels of indentation. Put the cursor at the end of the last line in the
block,  then type ENTER (or RETURN).  The cursor appears on the next line,
indented three levels like the previous line.

Now type some code, for example this line from the triply-indented block
in the *w* function in *sked.py*:

                bufname = bname(filename)

Following that, there is another block of code that is out-dented to 
only two levels of indentation.  Put the cursor at the end of the last
line in that block, then type ENTER.  The cursor moves to the next line,
correctly indented to two levels.
     
### Restore files from the demonstration ###

First, to prevent confusion, kill the buffers you just edited: *pmacs.py* and
*sked_fragments.py*

Next, delete those files from the *editors* directory:

    rm pmacs.py sked_fragments.py
    
If you want to run the demo again, you can copy the initial versions from
the *editors/demo* directory again.

Finally, restore the current version of *pmacs.py* from the *demo* directory:

    cp demo/pmacs.py .

Don't forget the final period!
    
The version of *pmacs.py* in *editors/demo* in the repository is the same as
the version in *editors*.   If you make changes in the current
*pmacs.py* that you commit to the repository, you must copy that revised *pmacs.py*
to the *demo* directory and commit it also.

Revised Sep 2024
