"""
check.py - check command line args and provide default args for ed.py

The commands and API for ed.py use the classic Unix ed conventions for
indexing and range (which are unlike Python): The index of the first
line is 1, the index of the last line is the same as the number of
lines (the length of the buffer in lines), and range i,j includes the
last line with index j (so the range i,i is just the line i, but it is
not empty).
"""

import parse

no_match = -99 # must be same as no_match in buffer.py

# Defaults and range checking, use the indexing and range conventions above.
# mk_ functions replace None missing arguments with default line numbers

def mk_iline(buf, iline):
    'Return iline if given, else return buf.dot, which is 0 if buffer is empty'
    return iline if iline != None else buf.dot

def mk_range(buf, start, end):
    'Return start, end if given, else return defaults'
    start = mk_iline(buf, start)
    return start, end if end != None else start

def iline_ok(buf, iline):
    'Return True if iline address is in buffer, always False for empty buffer'
    return isinstance(iline, int) and (0 < iline <= buf.nlines()) 

def iline_ok0(buf, iline):
    'Return True if iline address is in buffer, or buffer is empty'
    return isinstance(iline, int) and (0 <= iline <= buf.nlines())

def range_ok(buf, start, end):
    'Return True if start and end are in buffer, and start does not follow end'
    return iline_ok(buf, start) and iline_ok(buf, end) and start <= end

# The following functions check arguments, replace missing args with defaults, 
# and print error messages.

def iparam(s, default):
    """
    Return string s converted to int, if s is empty return default
    First returned value is False if nonempy s does not convert to int
    """
    if s:
        try:
            i = int(s)
            return True, i
        except:
            print('? integer expected at %s' % s)
            return False, default
    else:
        return True, default

def line_valid(buf, ok0, args):
    'check if iline in args is valid, if so return it along with any param'
    iline, _, param, _ = parse.arguments(args)
    iline = mk_iline(buf, iline)
    valid = iline_ok0(buf, iline) if ok0 else iline_ok(buf, iline)
    if not valid:
        print('? no match' if iline == no_match else '? invalid address')
    return valid, iline, param

def iline_valid(buf, args):
    'check if iline in args is valid, for cmds where line 0 is not valid: k z'
    return line_valid(buf, False, args)

def iline0_valid(buf, args):
    'check if iline in args is valid, for cmds where line 0 is valid: r a i'
    return line_valid(buf, True, args)

def irange(buf, args):
    'check range in args, for cmds that can affect a range of lines: p d c s'
    start, end, param, param_list = parse.arguments(args)
    start, end = mk_range(buf, start, end)
    valid = range_ok(buf, start, end)
    if not valid:
        print('? no match' if (start == no_match or end == no_match)
                else '? invalid address')
    param = param if param is not None else ''
    return valid, start, end, param, param_list

def range_dest(buf, args):
    'check range and destination in args, for cmds with a destination: m t'
    valid, start, end, params, _ = irange(buf, args)
    dest_valid, dest = None, None # placeholders needed for not valid case
    if valid:
        dest, _ = parse.line_address(buf, params)
        # dest can be 0 because lines are moved to *after* dest
        dest_valid = iline_ok0(buf, dest)
        if not dest_valid:
            print('? no match for destination' if dest == no_match else '? invalid destination')
    return (valid and dest_valid), start, end, dest
