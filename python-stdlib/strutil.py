"""
strutil.py - Our own implementations of CPython standard library str class
            methods that are not available in micropython.
            These have to be functions instead of methods.
"""

def ljust(line, width=80):
    """
    Our implemenation of the CPython stdlib ljust method in the str class.
    This has to be a function instead of a method, so instead of 
    'abc'.ljust(30) you have to write ljust('abc', 30) etc.
    Default line width is 80 so you can just write ljust('abc') for that.
    """             
    return line + (width - len(line))*' '

def expandtabs(line, tabsize=8):
    """
    Our implemenation of the CPython stdlib expandtabs method in the str class.
    This has to be a function instead of a method, so instead of 
    '\tabc'.expandtabs(4) you have to write expandtabs('\tabc',4) etc.
    Default tabsize is 8 chars so you can just write expandtabs('\tabc')
    """             
    return line.replace('\t', tabsize*' ')
