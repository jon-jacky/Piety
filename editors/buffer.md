
buffer.py
=========

**buffer.py** defines the *Buffer* class for line-oriented text editrs.

In this class, the text in the buffer is a list of strings
named *lines*.  Each string in the list is a single line of text that
ends with *\n*.  The *lines* list can be populated by calling the
standard Python file method *readlines* on a text file.

Many of the methods in the Buffer class correspond to *ed* commands and
the *ed.py* API.  The API (method calls) here use the classic Unix *ed*
conventions for indexing and range (which are unlike Python): The
index of the first line is 1, the index of the last line is the same
as the number of lines (the length of the buffer in lines), and range
i,j includes the last line with index j (so the range i,i is just the
line i, but it is not empty).  The buffer attribute named *dot* is the
index of the current line in the buffer, which is often used as the
text insertion point.

In this class each method has a fixed (positional) argument list,
provides no error checking, and no error messages or progress
messages.  This class has no print statements, and does not read or
write at the console.  This class only updates buffers and reads and
writes files.

This *Buffer* class provides a *write* method so other code can update
text buffers without using the *ed.py* user interface or API, simply
calling the standard Python *print* function, with the *file=...* optional
argument pointing to the buffer.

Revised Aug 2017