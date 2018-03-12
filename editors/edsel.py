"""
edsel - Display editor based on the line editor ed.py
   BUT import edo, ed + wyshka + samysh shell and scripting enhancements
"""

import traceback, os
import edo, wyshka, frame, display # display only used in cleanup()
from updates import Op
from updatecall import update

ed = edo.ed  # so we can call ed API without edo. prefix

def refresh():
    update(Op.refresh)

def do_window_command(line):
    'Window manager commands'
    param_string = line.lstrip()[1:].lstrip()
    if not param_string: # o: switch to next window
        next_i = (frame.ifocus+1 if frame.ifocus+1 < len(frame.windows)
                  else 0)
        ed.current = frame.windows[next_i].buf.name
        ed.buf = ed.buffers[ed.current]
        update(Op.next)
    elif param_string.startswith('1'): # o1: return to single window
        update(Op.single)
    elif param_string.startswith('2'): # o2: split window, horizontal
        update(Op.hsplit)
    else:
        print('? integer 1 or 2 expected at %s' % param_string) 

def do_command(line):
    'Process one command line without blocking.'
    line = line.lstrip()
    # try/except ensures we restore display, especially scrolling
    try:
        # Intercept special commands used by frame only, not ed.
        # Only in command mode!  Otherwise line might be text to add to buffer.
        if ed.command_mode and line == 'L': # similar to ^L
            refresh()
        elif ed.command_mode and line.startswith('o'):
            do_window_command(line)
        else:
            ed.do_command(line)
    except BaseException as e:
        cleanup() # so we can see entire traceback 
        traceback.print_exc() # looks just like unhandled exception
        ed.quit = True # exit() here raises another exception

# wyshka adds embedded python interpreter to do_command
_do_command = wyshka.wyshka(do_command=do_command,
                            command_mode=(lambda: ed.command_mode),
                            command_prompt=(lambda: ed.prompt))

# mk_x_do_command adds x execute script command to _do_command
_do_command = edo.mk_x_do_command(_do_command)

def startup(*filename, **options):
    'Configure ed for display editing, other startup chores'
    cmd_h = options['c'] if 'c' in options else 2
    ed.configure(update_fcn=update,  # replace ed's no-op update function
                 print_dest=open(os.devnull, 'w')) # discard l z printed output
    update(Op.rescale, start=cmd_h)  # rescale before ed.startup can call e()
    edo.startup(*filename, **options)

def cleanup():
    'Restore ed no display modes, full-screen scrolling, cursor to bottom.'
    ed.q()
    ed.configure() 
    display.set_scroll_all()
    display.put_cursor(frame.nlines,1)

def edsel(*filename, **options):
    """
    Top level edsel command to invoke from python prompt or command line.
    Won't work with cooperative multitasking, calls blocking input().
    """
    startup(*filename, **options)
    while not ed.quit:
        line = input((lambda: wyshka.prompt)())
        _do_command(line) # non-blocking
    cleanup()

# initialize first window only once on import
frame.init(ed.buf) # import ed above initializes ed.buf

if __name__ == '__main__':
    filename, options = ed.cmd_options()
    edsel(*filename, **options)
