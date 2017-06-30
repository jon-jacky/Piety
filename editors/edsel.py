"""
edsel - Display editor based on the line editor ed.py.  
         Described in ed.md and edsel.md.
"""

import traceback, os
import ed, frame, display # display only used in cleanup()
from updates import update, Op

def do_window_command(line):
    param_string = line.lstrip()[1:].lstrip()

    if not param_string: # o: switch to next window
        next_i = (frame.win_i+1 if frame.win_i+1 < len(frame.windows)
                  else 0)  # FIXME?  Define frame.next_window() - ?
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
        # Intercept special commands used by frame only, not ed
        # Only in command mode!  Otherwise line is text to add to buffer.
        if ed.command_mode and line.lstrip().startswith('o'):
            do_window_command(line)
        else:
            ed.do_command(line) # non-blocking
        frame.handle_updates()
    except BaseException as e:
        cleanup() # so we can see entire traceback 
        traceback.print_exc() # looks just like unhandled exception
        exit()

def startup(*filename, **options):
    ed.configure(cmd_fcn=do_command, # so x uses edsel not ed do_command()
                 print_dest=open(os.devnull, 'w')) # discard l z printed output
    ed.startup(*filename, **options)
    cmd_h = options['c'] if 'c' in options else None
    frame.init(ed.buf, cmd_h_option=cmd_h) # ed.startup() above inits ed.buf

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

if __name__ == '__main__':
    filename, options = ed.cmd_options()
    main(*filename, **options)
