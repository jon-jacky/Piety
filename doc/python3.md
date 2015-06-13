
Python 3
========

**Piety** is written in Python 3.  Piety was developed in Python 2
through May 2015.  The final Python 2 version is stored in this
repository under the *python2* tag.  Python 3 development in *master*
and other branches began in June 2015.

This page describes the Python 2 to Python 3 conversion.

At the end of May 2015, the *python2* tag was created from the
*master* branch.  A *2to3* branch was created and the conversion was
done there, using the *2to3* program.  In early June 2015, the *2to3*
branch was merged back into *master* and then deleted.

### Automatic conversion ###

Most of the conversion was performed automatically by the *2to3*
program.  Almost all of the changes merely added parentheses to
*print* statements.  In addition, the *2to3* program made these
changes:

  --- editors/ed0.py	    (original)
  +++ editors/ed0.py	    (refactored)
  ...      ...
  -        keys = buffers.keys()
  +        keys = list(buffers.keys())

  --- shell/pysh.py	    (original)
  +++ shell/pysh.py	    (refactored)
  ...
  -                exec command in globals
  +                exec(command, globals)
  ...
  -        command = raw_input('>> ')
  +        command = input('>> ')

The *2to3* program also replaced *raw_input* with *input* in *ed.py*
and *edd.py*.  Those were the only changes made by *2to3*.  Some
Python source files were not changed at all.

### Manual conversion ###

In Python 2 the division operator */* applied to two integers performs
"floor division" which always produces an integer result (so *1/2*
produces *0*), while in Python 3 the same operator applied to the same
two integers performs "true division" which may produce a floating
point result (so *1/2* produces *0.5*).   Python 3 provides a new
floor division operator *//* (so *1//2* produces *0*).

The *2to3* program does not automatically replace */* with the new
*//* operator in integer division; it does not even warn where the
behavior may have changed.  When testing the converted program
*edd.py*, we found three lines where the intended behvior requires
floor division, for example:

        seg_1 = buf.dot - win_h//2  # must use // floor division here

We made these changes by hand.

### Scripts that use the python command ###

On our development system at this time, the *python* command invokes
Python 2 and the *python3* command invokes Python 3.  So we have to
provide special treatment for scripts that use the *python* command.

In the *scripts* directory, the *piety* script (for example) has a
hashbang line: *#!/usr/bin/env python*, so the script name can be used
as a command.  To run this script in Python 3, we use the command
*python3 piety*, which invokes *python3* and ignores the hashbang
line.

Some of the scripts under the *test* directory are shell scripts that
invoke Python, for example: *python -c "import ed; ed.main()"*.  To
run these scripts with Python 3, we edit them to replace the *python*
command: *python3 -c ...* etc.  (The edited scripts are not stored in
this repository.)

Revised June 2015
