"""
util.py - miscellaneous utilities 
          - that are not platform-dependent or configuration-dependent
          - that are used by modules in more than one directory
"""

def putstr(s):
    """
    Print string (can be just one character) on console with no
    formatting (unlike plain Python print).  Flush to force output immediately.
    If you want newline, you must explicitly include it in s.
    """
    # In python3 this can be expressed in pure Python
    print(s, end='', flush=True)
