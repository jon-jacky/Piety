"""
edsel - Display editor based on the line editor ed.py.  
         Described in ed.md and edsel.md.
"""

import traceback, os
import ed, frame, display # display only used in cleanup()

# ed command names used in update_display - FIXME use Op
# ed.cmd_name = ''   # FIXME unnecessary?  Occurs in ed.py already

def do_command(line):
    'Process one command line without blocking.'
    # try/except ensures we restore display, especially scrolling
    try:
        # FIXME the next two lines should disappear when we handle update Op
        # For now we have two top-level calls in frame, o() and handle_updates
        frame.cmd_h0, frame.win0 = frame.cmd_h, frame.win # save parameters before call ed.cmd
        frame.o_cmd = ed.cmd_name = ''  # must clear before call ed.cmd
        # Intercept special commands used by frame only, not ed
        # Only in command mode!  Otherwise line is text to add to buffer.
        if ed.command_mode and line.lstrip().startswith('o'):
            frame.o(line) # window commands, assigns o_cmd
        else:
            ed.do_command(line) # non-blocking
        frame.handle_updates()
    except BaseException as e:
        cleanup() # so we can see entire traceback 
        traceback.print_exc() # looks just like unhandled exception
        exit()

def startup(*filename, **options):
    # must call configure() first, startup() uses update_fcn 
    ed.configure(cmd_fcn=do_command, # so x uses edsel not ed do_command()
                 print_dest=open(os.devnull, 'w'), # discard l z printed output
                 update_fcn=frame.update) # post display updates
    ed.startup(*filename, **options)
    cmd_h = options['c'] if 'c' in options else None
    frame.init(ed.select_buf, ed.buf, cmd_h) # ed.startup() just above initializes ed.buf

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
