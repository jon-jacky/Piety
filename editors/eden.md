
eden
====

**eden** is a display editor in pure Python based on the line editor
  [ed.py](ed.md) and the display editor [edsel.py](edsel.md).

**eden** works like *edsel* but also adds an on-screen editing mode
  that (currently) works on just a single line at a time.
  When you type the classic *ed* *c* (change) command without address
  arguments, *eden* puts the cursor at the beginning of the line at
  dot.  You can then move the cursor and edit within that line as
  described [here](../console/command.txt), and add
  text anywhere within that line just by typing.  When you are 
  finished editing that line, simply type RETURN to return to 
  command mode.
  
  When the *c* command is used with address arguments, it behaves
  as in classic *ed*.  In particular, *.c* (*dot* *c*) deletes and
  then replaces the single line at dot.

Revised November 2016
