"""
test_terminal.py - demonstrate single character input, output to console

 python -i test_terminal.py
piety>abcd
abcd
>>> test()
piety>efgh
efgh
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

if __name__ == '__main__':
    test()



