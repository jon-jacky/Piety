"""
test_console_blocking.py - demonstrate single character input, output to console

 $ python -i test_console_blocking.py
piety> abcd
abcd
piety> 
>>> test()
piety> efgh
efgh
piety> 
>>> 

"""

import terminal, console

c0 = console.Console() # all default args

def test():
    """ 
    loop calling getchar until line terminator, then print buffer contents
    """
    c0.restart() # includes terminal.setup()
    ch = 'x' # anything but c0.terminator
    while not ch == c0.terminator:
        ch = c0.getchar() # also updates c0.cmdline
        # terminal.putstr(ch) # echo in place  NOT! We have default echo=True
    terminal.restore()
    print # resume on next line

if __name__ == '__main__':
    test()


