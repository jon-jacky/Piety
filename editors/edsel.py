"""
edsel - Display editor based on the line editor ed.py.  
"""

import traceback, os
import ed, frame, display # display only used in cleanup()
from updates import Op
from updatecall import update

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
    # try/except ensures we restore display, especially scrolling
    try:
        # Intercept special commands used by frame only, not ed.
        # Only in command mode!  Otherwise line might be text to add to buffer.
        if ed.command_mode and line.lstrip() == 'L': # similar to ^L
            refresh()
        elif ed.command_mode and line.lstrip().startswith('o'):
            do_window_command(line)
        else:
            ed.do_command(line) # non-blocking
    except BaseException as e:
        cleanup() # so we can see entire traceback 
        traceback.print_exc() # looks just like unhandled exception
        ed.quit = True # exit() here raises another exception

def startup(*filename, **options):
    'Configure ed for display editing, other startup chores'
    cmd_h = options['c'] if 'c' in options else None
    ed.configure(cmd_fcn=do_command, # so x uses edsel not ed do_command()
                 update_fcn=update,  # replace ed's no-op update function
                 print_dest=open(os.devnull, 'w')) # discard l z printed output
    update(Op.rescale, start=cmd_h)  # rescale before ed.startup can call e()
    ed.startup(*filename, **options)

def cleanup():
    'Restore full-screen scrolling, cursor to bottom.'
    display.set_scroll_all()
    display.put_cursor(frame.nlines,1)

def main(*filename, **options):
    """
    Top level edsel command to invoke from python prompt or command line.
    Won't work with cooperative multitasking, calls blocking input().
    """
    startup(*filename, **options)
    while not ed.quit:
        prompt_string = ed.prompt if ed.command_mode else ''
        line = input(prompt_string) # blocking
        do_command(line) # non-blocking
    cleanup()

# initialize first window only once on import
frame.init(ed.buf) # import ed above initializes ed.buf

if __name__ == '__main__':
    filename, options = ed.cmd_options()
    main(*filename, **options)
