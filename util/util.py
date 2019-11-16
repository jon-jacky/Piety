"""
util.py - miscellaneous utilities 
          - that are not platform-dependent or configuration-dependent
          - that are used by modules in more than one directory
"""

def putstr(s):
    """
    Print string (can be just one character) on stdout with no
    formatting (unlike plain Python print).  Flush to force output immediately.
    If you want newline, you must explicitly include it in s.
    Prints to stdout, which may be redirected.
    """
    print(s, end='', flush=True)

