"""
aterminal.py - experiments with asynchronous termimal code.
"""

import asyncio 

import terminal as term # Piety

async def agetchar():
   return await asyncio.to_thread(term.getchar)

# Test, based on main in Piety/unix/terminal.py
 
async def main():
    c = line = ''
    term.set_char_mode() # enter single character more
    term.putstr('> ')
    while not c == '\r':
        c = await agetchar()
        term.putstr(c)
        line += c
    term.set_line_mode() # return to normal mode
    print()
    print(line)

if __name__ == '__main__':
    asyncio.run(main())
  
