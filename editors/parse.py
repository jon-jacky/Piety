"""
parse.py - command line parsing for ed.py
"""

import re

complete_cmds = 'AbBdDeEfjIJkKlmnNOpqQrsStTwxyz' # commands that do not use input mode
input_cmds = 'aci' # commands that use input mode to collect text
ed_cmds = complete_cmds + input_cmds

# regular expressions for line address forms and other command parts
number = re.compile(r'(\d+)')
fwdnumber = re.compile(r'\+(\d+)')
bkdnumber = re.compile(r'\-(\d+)')
bkdcnumber = re.compile(r'\^(\d+)')
plusnumber = re.compile(r'(\++)')
minusnumber = re.compile(r'(\-+)')
caratnumber = re.compile(r'(\^+)')
# string search, regexp meta chrs match themselves
fwdsearch = re.compile(r'/(.*?)/') # non-greedy *? for /text1/,/text2/
bkdsearch = re.compile(r'\?(.*?)\?')
# regular expression search, unescaped regexp meta chrs are interpreted
refwdsearch = re.compile(r'\|(.*?)\|')
rebkdsearch = re.compile(r'&(.*?)&')
text = re.compile(r'(.*)') # nonblank
mark = re.compile(r"'([a-z@])")  # 'c, ed mark with single lc char label or @

def line_address(buf, cmd_string):
    """
    Return line number for address at start of cmd_string (None of not found),
     also return rest of cmd_string.
    This is where we convert the various line address forms to line numbers.
    All other code in ed.py and related modules uses line numbers only.
    """
    if cmd_string == '':
        return None, ''
    if cmd_string[0] == '.': # current line
        return buf.dot, cmd_string[1:]
    if cmd_string[0] == '$': # last line
        return buf.nlines(), cmd_string[1:]
    if cmd_string[0] == ';': # equivalent to .,$  - current line to end
        return buf.dot, ',$'+ cmd_string[1:]
    if cmd_string[0] in ',%': # equivalent to 1,$ - whole buffer
        return 1, ',$'+ cmd_string[1:]

    # These next two cases don't return, instead they proceed to next section

    if cmd_string[0] in '[': # equivalent to '@,- -selection from mark to dot
        cmd_string = "'@,-" + cmd_string[1:]

    # This is a special case, we find two line numbers at once.
    if cmd_string[0] in ']': # paragraph
        cmd_string = "%d,%d" % (buf.para_first(), buf.para_last()) + cmd_string[1:]

    m = number.match(cmd_string) # digits, the line number
    if m:
        return int(m.group(1)), cmd_string[m.end():]
    m = fwdnumber.match(cmd_string) # +digits, relative line number forward
    if m:
        return buf.dot + int(m.group(1)), cmd_string[m.end():]
    m = bkdnumber.match(cmd_string) # -digits, relative line number backward
    if m:
        return buf.dot - int(m.group(1)), cmd_string[m.end():]
    m = bkdcnumber.match(cmd_string) # ^digits, relative line number backward
    if m:
        return buf.dot - int(m.group(1)), cmd_string[m.end():]
    m = plusnumber.match(cmd_string) # + or ++ or +++ ...
    if m:
        return buf.dot + len(m.group(0)), cmd_string[m.end():]
    m = minusnumber.match(cmd_string) # digits, the line number
    if m:
        return buf.dot - len(m.group(0)), cmd_string[m.end():]
    m = caratnumber.match(cmd_string) # digits, the line number
    if m:
        return buf.dot - len(m.group(0)), cmd_string[m.end():]
    # string search, regexp meta chrs match themselves
    m = fwdsearch.match(cmd_string)  # /text/ or // - forward search
    if m:
        return buf.F(re.escape(m.group(1))), cmd_string[m.end():]
    m = bkdsearch.match(cmd_string)  # ?text? or ?? - backward search
    if m:
        return buf.R(re.escape(m.group(1))), cmd_string[m.end():]
    # regular expression search, unescaped regexp meta chrs are interpreted
    m = refwdsearch.match(cmd_string)  # |text| or || - forward regexp search
    if m:
        return buf.F(m.group(1)), cmd_string[m.end():]
    m = rebkdsearch.match(cmd_string)  # &text& or && - backward regexp search
    if m:
        return buf.R(m.group(1)), cmd_string[m.end():]
    m = mark.match(cmd_string) # 'c mark with single lc char label
    if m:
        c = m.group(1)
        i = buf.mark[c] if c in buf.mark else -9999 # invalid address
        return i, cmd_string[m.end():]
    return None, cmd_string

def command_tokens(buf, cmd_string):
    """
    Parse ed.py command string, return multiple values in this order:
     cmd_name - single-character command name
     start, end - integer line numbers
     params - string containing other command parameters
    All are optional except cmd_name, assign None if an item is not present
    """
    cmd_name, start, end, params = None, None, None, None
    # look for start addr, optional. if no match start,tail == None,cmd_string
    start, tail = line_address(buf, cmd_string)
    # look for end address, optional
    if start != None:
        if tail and tail[0] == ',': # ',' means next addr is NOT optional
            end, tail = line_address(buf, tail[1:]) # reassign tail
            if end == None:
                print('? end address expected at %s' % tail)
                return 'ERROR', start, end, params
    # look for cmd_string, NOT optional
    if tail and tail[0] in ed_cmds:
        cmd_name, params = tail[0], tail[1:].strip()
    # special case command names
    elif tail == '' or tail.isspace():
        cmd_name = 'l' # default for empty cmd_string
    elif tail[0] == '=':
        cmd_name = 'A'
    else:
        print('? command expected at %s' % tail)
        return 'ERROR', start, end, params
    # command-specific parameter parsing
    # literal string replace with s/old/new/g, g optional
    if cmd_name == 's' and len(params.split('/')) == 4:
        use_regex = False
        empty, old, new, glbl = params.split('/') # glbl == '' when g absent
        return cmd_name, start, end, old, new, glbl, use_regex
    # regular expression string replace with s|old|new|g, g optional
    elif cmd_name == 's' and len(params.split('|')) == 4:
        use_regex = True
        empty, old, new, glbl = params.split('|') # glbl == '' when g absent
        return cmd_name, start, end, old, new, glbl, use_regex
    # all other commands, no special parameter parsing
    else:
        # return each space-separated parameter as separate arg in sequence
        return (cmd_name,start,end) + (tuple(params.split() if params else ()))

def command(buf, line):
    'Wrap command_tokens, provide necessary but banal pre/post-processing'
    cmd_string = line.lstrip()
    if cmd_string and cmd_string[0] == '#': # comment, do nothing
        return None
    items = command_tokens(buf, cmd_string)
    if items[0] == 'ERROR':
        return None # parse.command_tokens already printed error message
    else:
        tokens = tuple([ t for t in items if t != None ])
    cmd_name, args = tokens[0], tokens[1:]
    return cmd_name, args

def arguments(args):
    """
    Parse variable-length argument list for ed.py Python API, all args optional
    Return fixed length tuple: start, end, text, params
    start, end are line numbers, for example the first and last line of region.
    When present, start and end are int, both might be absent, indicated None.
    text is the first token in the parameter list, str or None if absent
    params is the parameter list, [] if absent.
    """
    # get 2, 1, or 0 optional line numbers from head of args list
    if len(args) > 1 and isinstance(args[0],int) and isinstance(args[1],int):
        start, end, params = int(args[0]), int(args[1]), args[2:]
    elif len(args) > 0 and isinstance(args[0],int):
        start, end, params = int(args[0]), None, args[1:]
    else:
        start, end, params = None, None, args
    # get 1 or 0 optional strings and the rest of args list
    if params and isinstance(params[0], str):
        text, params = params[0], params[1:]
    else:
        text = None 
    return start, end, text, params # params might still be non-empty
