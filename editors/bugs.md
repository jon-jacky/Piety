
bugs
====

Unfixed bugs in the editors.  At this time (Nov 2024) we know of two:

- **frame-scrolls-up**: Sometimes when an editor writes a message 
  in the srolling REPL region, the entire frame scrolls up, as if
  the scrolilng region were the whole terminal window, not just
  the REPL lines at the bottom,.
  
  The workaround for this is to invoke *refresh_all* by typing *M-l*
  (hold the *alt* key while typing the *L* key).  This restores all the
  frame contents to their correct locations and resets the scrolling region.

- **junk-in-yank*:  Sometimes invoking *yank* by typing *C-y* (hold the
  *ctrl* key while typing the *Y* key) pastes in some additional text 
  from earlier *kill-line* *C-k* commands, in addition to the intended
  text from the immediately preceding *cut* or *kill-line*.
  
  The workaround for this is to simply delete the unwanted text.
  
Revised Nov 2024

 
