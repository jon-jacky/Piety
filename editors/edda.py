"""
edda - Display editor based on the line editor ed.py

"""

import traceback, os, sys
import edo, frame, wyshka, samysh, buffer
import storage as st

ed = edo.ed  # so we can use ed API without prefix

# edda API functions

def L():
    'Refresh'
    frame.refresh(1) # start at column 1

def o(*args):
    'Window commands: o(2) horiz. split, o(1) one window, o() next window'
    if not args:
        win = frame.next()
        st.buf = win.buf
        st.current = st.buf.name
    elif args[0] == 1:
        frame.single()
    elif args[0] == 2:
        frame.hsplit()

def h(*args):
    'Resize/balance frame: h(n) set scrolling region to n lines, h() balance only'
    if args:
        frame.cmd_h = args[0]
    frame.rescale(None) # use frame.cmd_h

# Wrappers for API functions

def do_rescale_command(paramstring):
    'Change n of lines in scrolling command region, or balance windows'
    if paramstring:
        try:
            nlines = int(paramstring)
            h(nlines)
        except ValueError:
            pass # keep current nlines, but .rescale balances windows
    else:
        h()

def do_window_command(paramstring):
    'Window manager commands'
    if not paramstring: # o: switch to next window
        o()
    elif paramstring.startswith('1'): # o1: return to single window
        o(1)
    elif paramstring.startswith('2'): # o2: split window, horizontal
        o(2)
    else:
        print('? integer 1 or 2 expected at %s' % paramstring)


def do_command(line):
    'Process one command line without blocking.'
    line = line.lstrip()
    paramstring = line[1:].lstrip()
    # try/except ensures we restore display, especially scrolling
    try:
        # Intercept special commands used by frame only, not ed.
        if line.startswith('L'):
            L()
        elif line.startswith('h'):
            do_rescale_command(paramstring)
        elif line.startswith('o'):
            do_window_command(paramstring)
        else:
            edo.do_command(line)
    except BaseException as e:
        cleanup() # so we can see entire traceback
        traceback.print_exc() # looks just like unhandled exception
        ed.quit = True # exit() here raises another exception

# We redefined do_command so we have to redefine process_line
def base_process_line(line):
    'process one line without blocking, according to mode'
    if ed.command_mode:
        do_command(line)
    else:
        ed.add_line(line)

# Add embedded python interpreter.
_process_line = wyshka.shell(process_line=base_process_line,
                             command_mode=(lambda: ed.command_mode),
                             command_prompt=(lambda: ed.prompt))

# Add command to run script from buffer with optional echo and delay.
process_line = samysh.add_command(edo.X_command(_process_line), _process_line)

def startup(*filename, **options):
    'Configure ed for display editing, other startup chores'
    global cmd_h
    if 'c' in options:
        cmd_h = options['c']
    frame.rescale(cmd_h) # before edo.startup calls e()
    # Enable display in ed, buffer, storage modules. Defaults is no display.
    ed.displaying = buffer.displaying = st.displaying = True
    ed.frame = buffer.frame = st.frame = frame
    edo.startup(*filename, **options)
    if filename:
        frame.insert(1, frame.win.buf.dot)

def cleanup():
    'Restore display screen then turn off display updates etc.'
    frame.restore()
    ed.displaying = buffer.displaying = st.displaying = False
    ed.frame = buffer.frame = st.frame = None
    ed.lz_print_dest = sys.stdout

def main(*filename, **options):
    'Top level edda command to invoke from python prompt or command line.'
    startup(*filename, **options)
    while not ed.quit:
        line = input(wyshka.prompt)
        process_line(line)
    cleanup()

# initialize scrolling region and first window only once on import
cmd_h = 2
frame.init(st.buf) # import ed above initializes st.buf

if __name__ == '__main__':
    filename, options = ed.cmd_options()
    main(*filename, **options)
