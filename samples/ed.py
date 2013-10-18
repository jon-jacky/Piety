"""
ed.py - ed is the standard text editor

Simple line editor for Python.  It can run as a standalone program,
but is intended to run within an interactive Python session.  It can
run concurrently with other tasks in the session, under a cooperative
multitasking scheduler such as Piety.

Our ed.py is based on the classic Unix editor ed.  For a description
of Unix ed, just do man ed on any Unix-like system.  Or see the book
The Unix Programming Environment by Kernighan and Pike or the Software
Tools books by Kernighan and Plauger.

We augment classic ed by supporting multiple buffers and files, using
commands based on sam, a later Unix editor.

Here is how to use ed to start a new (empty) file, put some text in
the file, and save it:

 >>> import ed  
 >>> ed.cmd() 
 :a
 The colon : is the ed command prompt.
 Use the 'a' command to insert ('append') text,
 the 'w' command to save ('write') the text to a file,
 and 'q' to exit ed.
 End the text with a period by itself at the start of a line.
 .
 :w
 :q
 >>>

"""





