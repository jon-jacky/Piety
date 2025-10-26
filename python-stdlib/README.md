
python-stdlib
=============

Some of these are files copied (and sometimes edited) from 
*.../micropython-lib/python-stdlib* in the micropython distribution. 
The files are copied here because:

- Some of the files need to be edited to work in micropython, even
  though they come from micropython.org.
    
- Files here are kept under version control and are backed up 
  along with the other Piety sources.

Other files here are new because:

- File contain new functions we had to write to replace 
  functions or methods present in CPython but absent from micropython  

### Files ###

- **path.py**: Copied without changes

- **string.py**: Copied without changes

- **strutil.py**: New file with functions *expandtabs* and *ljust* 
    to replace *str* methods present in CPython, absent in micropython

- **textwrap.py**: Copied, then edited to avoid *ValueError: regex too complex*

Revised Oct 2025
