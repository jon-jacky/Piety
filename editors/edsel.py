"""
edsel - Display editor based on the line editor ed.py
   BUT import edo, ed + wyshka + samysh shell and scripting enhancements
"""

import traceback, os
import edo, frame, display, config, updatecall, wyshka, samysh # FIXME display only used in cleanup(), frame shouldn't be needed
from updates import Op

ed = edo.ed  # so we can call ed API without edo. prefix

def refresh():
    config.update(Op.refresh)

def do_window_command(line):
    'Window manager commands'
    parastring = line.lstrip()[1:].lstrip()
    if not parastring: # o: switch to next window
        next_i = (frame.ifocus+1 if frame.ifocus+1 < len(frame.windows)
                  else 0)
        ed.current = frame.windows[next_i].buf.name
        ed.buf = ed.buffers[ed.current]
        config.update(Op.next)
    elif parastring.startswith('1'): # o1: return to single window
        config.update(Op.single)
    elif parastring.startswith('2'): # o2: split window, horizontal
        config.update(Op.hsplit)
    else:
        print('? integer 1 or 2 expected at %s' % parastring) 

def base_do_command(line):
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
_do_command = wyshka.shell(do_command=base_do_command,
                           command_mode=(lambda: ed.command_mode),
                           command_prompt=(lambda: ed.prompt))

# do_command: add edo.x_command that executes script using samysh
do_command = samysh.add_command(edo.x_command(_do_command), _do_command)

def startup(*filename, **options):
    'Configure ed for display editing, other startup chores'
    global cmd_h
    if 'c' in options:
        cmd_h = options['c'] 
    updatecall.update(Op.rescale, start=cmd_h) # before edo.startup calls e()
    edo.startup(*filename, **options)
    config.lz_print_dest = config.null # reassign configs made in edo.startup
    config.update = updatecall.update

def cleanup():
    'Restore full-screen scrolling, cursor to bottom.'
    ed.q()
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
        do_command(line) # non-blocking
    cleanup()

# initialize scrolling region and first window only once on import
cmd_h = 2
frame.init(ed.buf) # import ed above initializes ed.buf

if __name__ == '__main__':
    filename, options = ed.cmd_options()
    edsel(*filename, **options)
