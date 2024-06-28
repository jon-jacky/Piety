"""
aterminal.py - Read characters from the terminal in the asyncio event loop.

...$ python3 aterminal.py # To run once. Type some characters, then RET (or Enter)
> abcdef
abcdef
...$

...$ python3 -i  # To run multiple times.  main() does not call loop.close().
>>> import aterminal
>>> aterminal.main()
> abcdef
abcdef
>>> aterminal.main()
> ghijkl
ghijkl
>>> 

"""

import sys, asyncio
import terminal as term

tl = term.set_line_mode # Type tl() to restore terminal echo etc. after a crash.

loop = asyncio.get_event_loop()
  
line = ''

def setup():
    'Initialize empty line, set terminal to raw single char mode, print prompt.'
    global line
    line = ''
    term.set_char_mode()
    term.putstr('> ')  # We want to see this *before* the first character is typed.

def cleanup():
    'Stop the event loop, but dont close it. Restore term line mode, print line.'
    loop.stop() # escape from run_forever()
    term.set_line_mode()
    print() # must advance to next line
    print(line)

def runcmd(c):
    'Add single character to line.  Test for exit char - if found, call cleanup.'
    global line
    term.putstr(c)
    line += c
    if c in '\n\r':
         cleanup()

def handler():
    'Run each time sys.stdin detects a new character.  Read the char, call runcmd.'
    c = term.getchar()
    runcmd(c)

loop.add_reader(sys.stdin, handler) # FIXME?  Use tty not stdin, as in display.py?

def main():
    'Call setup and start the event loop.  Event loop was created at module level.'
    setup()
    loop.run_forever()

if __name__ == '__main__': 
    main()
    loop.close()

