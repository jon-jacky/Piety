
branches
========

This is the *rewrite* branch.

Beginning in Feb 2023, a total rewrite of the Piety system is underway
here in the *rewrite* branch and its branches, to shorten and simplify 
the code, and improve the responsiveness of the programming environment.

Recent work in the *rewrite* branch:

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

Revised Jul 2023
