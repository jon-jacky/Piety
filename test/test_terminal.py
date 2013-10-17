"""
test_terminal.py - demonstrate single character input, output to console

 ...$ python -i path.py
 >>> import test_terminal
 >>> test_terminal.test()
 piety> ... type characters, then RETURN ...
 ... prints string of the characters you typed ...
 >>>

"""

import terminal

terminator = '\r'  # RETURN key

def test():
    """ 
    loop calling getchar until line terminator, then print buffer contents
    """
    terminal.setup()
    print 'piety>',
    ch = 'x'
    line = str()
    while not ch == terminator:
        ch = terminal.getchar()
        terminal.putstr(ch) # echo in place
        line += ch # yes, I know this is inefficient
    terminal.restore()
    print # resume on next line
    print line



