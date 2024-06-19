"""
aterminal.py - experiments with asynchronous termimal code.
"""

import sys
import asyncio as aio 
import terminal as term

loop = aio.get_event_loop()
  
line = ''

def setup():
    global line
    start = False
    line = ''
    term.set_char_mode()
    term.putstr('> ')  # We want to see this *before* the first character.

def cleanup():
    loop.stop() # escape from run_forever()
    term.set_line_mode()
    print() # must advance to next line
    print(line)

def runcmd():
    'Run this each time sys.stdin sees a new character.'
    global line
    c = term.getchar()
    term.putstr(c)
    line += c
    if c == '\r':
         cleanup()
      
loop.add_reader(sys.stdin, runcmd)

def main():
    setup()
    loop.run_forever()

if __name__ == '__main__':
    main()
    loop.close()

