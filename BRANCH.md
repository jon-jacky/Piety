
branches
========

This is the *rewrite* branch.

Beginning in Feb 2023, a total rewrite of the Piety system is underway
here in the *rewrite* branch and its branches, to shorten and simplify 
the code, and improve the responsiveness of the programming environment.

The *rewrite* branch is now the main branch.  I will never merge it back
into the *master* branch.

Recent work in the *rewrite* branch:

-  7 Aug 2024: Merge the *eventloop* branch back into the *rewrite* branch.

- 16 Jun 2024: Begin *eventloop* branch to make coroutine versions of the 
  *pysh* custom Python interpreter and *pmacs* editor, that can run 
  as concurrent tasks in an *asyncio* event loop.

-  2 Jun 2024: Reorganize directories.  Split *tasks* directory into 
  three: *tasking*, *threads*, and *coroutines*, rename *shells* to *python*.
 
- 27 May 2024: Begin experimenting with coroutines in the *tasks* directory,
  still in the *rewrite* branch.
  
- 24 May 2024: Finished for now adding and reorganizing links on Python
  language compilers, libraries, and tools in *doc/compilers.md* and
  *utilities.md*.

- 11 May 2024: Change default branch at Github from *master* to *rewrite*.

- 11 May 2024: Finish revising .md files at top level and under *doc*.

-  9 May 2024: Begin revising top-level *README.md* and other *.md* files
   at top level and under *doc* to make them consistent with code in
   the *rewrite* branch.  Do this work in the *rewrite* branch.

-  9 May 2024:  Revise top-level README.md in *master* branch:
   put directions to *rewrite* branch right at the top so they
   can't be missed.
 
-  9 May 2024:  Finish work on tasking with threads for now.  Already in 
   the *rewrite* branch, so no merge is needed.
 
- 23 Apr 2024:  Resume work on tasking with threads, but in the *rewrite* branch.

- 18 Apr 2024:  Finish fixing editor bugs for now.  Merge *edfix* branch
  back into *rewrite* branch.

- 9 Apr 2024: Begin *edfix* branch to fix bugs recently found in the editors. 

- 9 Apr 2024: Finish work on the custom Python REPL and tasking code 
  for now.  Merge *pysh* branch back into *rewrite* branch.

- 27 Feb 2024: Begin *pysh* branch to provide a custom Python REPL that
  uses our *editline* so we can restore the cursor to the correct
  position in the command line after another thread moves it.
 
- 27 Feb 2024: Finish experiments with threading for now.  Merge 
  *tasks* branch back into *rewrite* branch.

- 12 Jan 2024: Begin *tasks* branch off *rewrite* brnach for experiments 
  with tasks and  concurrency using Python threads.

- 12 Jan 2024: Finish work on the editors for now.  Merge *ed* branch
  back into *rewrite* branch.

- 11 Jan 2024: Multiple windows working in edsel, dmacs, and pmacs.
  Merge *window* branch back into *ed* branch.

- 21 Oct 2023: Make *window* branch to *ed* branch.  Add multiple windows
  to *pmacs* editor.

- 21 Oct 2023: Merge *ed* branch back into *rewrite* branch.  However, 
  work continues in the *ed* branch and its branches.

- 21 Oct 2023: *pmacs* emacs-like editor working.  Merge *editline* branch 
  back into *ed* branch, with completed *editline* and *pmacs* modules.  

- 13 Jul 2023: make *editline* branch to *ed* branch.
  Add *editline* module, edit and display a string using readline control keys.
  Add *pmacs*, edit text in lines anywhere in buffer, not just in append mode. 

- 2 Jul 2023: Merge *ed* branch back into *rewrite* branch.  However, 
  work continues in the *ed* branch and its branches.

- 1 Jul 2023: dmacs editor working (no longer called pmacs), merge 
  *pmacs* branch back into *ed* branch.

- 28 May 2023: Make *pmacs* branch to *ed* branch to invoke editor functions
  with emacs keycodes so you don't have to invoke the functions from the 
  Python REPL.

- 28 May 2023: Indent, wrap, and join functions working, merge *format*
  branch back into *ed* branch.

- 19 May 2023: Make *format* branch of *ed* branch to add indent and 
  wrap functions to *sked* and *edsel*.

- 19 May 2023: rename *frame.py* and *frameinit.py* to *edsel.py* and
  *edselinit.py*.

- 12 May 2023: revised a(ppend) command now working, merge *inwindow* branch
  back into *ed* branch.

- 22 Apr 2023: Make *inwindow* branch of *ed* branch to work on display code:
   Type lines into the a (append) command in place in the display window.

- 22 Apr 2023: Revise editors/README.md to describe recent work on
   *sked* and *frame* in the *patch* and *fparam* branches.

- 20 Apr 2023: All sked functions are now displaying in the *fparam* branch,
   merge back into the *ed* branch.

-  8 Apr 2023 Make *fparam* branch of *ed* branch to work on display code.
   Instead of patching functions in *sked*, display functions are passed 
   as parameters to functions in *sked*.

-  8 Apr 2023: Reach stopping place in *patch* branch, merge back into *ed*.

- 20 Feb 2023: Make *patch* branch of *ed* branch to work on display code 
   in *frame*.  Display functions are assigned to ('patch') placeholder
   functions in *sked*.

-  9 Feb 2023: Remove *shells* directory and *pycall*, not needed.

-  2 Feb 2023: Make the *ed* branch for work on our line editor *sked.py*.

-  1 Feb 2023: Add *shells* directory with *pycall* callable Python interpreter.

-  1 Feb 2023: Delete most files and directories for a fresh start.
   Revise *BRANCH.md*, *DIRECTORIES.md*, and *bin/paths*.

