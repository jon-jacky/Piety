"""
wyshka.py - Shell that can alternate between pysh (Python)
            and the command line interface to another application program,
            such as ed.  You can use Python without leaving the application.
"""

import pysh, ed, buffer, display
from contextlib import redirect_stdout

# globals reassigned by shell _process_line below
python_mode = False
prompt = ''

def shell(process_line=(lambda line: None), command_mode=(lambda: True), 
          command_prompt=(lambda: '')):
    """
    Return a shell: a function with one argument (a string, the
    command line) that sends a command either to Python or to another
    application.

    This function has three optional keyword arguments with defaults:

    process_line is a callable with one string argument that performs
    the application's action.  It might execute a command line or 
    add a text line to a buffer.

    command_mode is a callable with no arguments that returns True
    when the application is in a state where its command interpreter
    can be replaced by Python.  Default always returns True.

    command_prompt is a callable with no arguments that returns the
    application prompt string, which might depend on application
    state.  Default always returns the empty string.
    """
    def _process_line(line):
        global python_mode, prompt
        if command_mode():

            # set up redirect
            prefix = ''
            if line and line[0] in '!:':
                prefix = line[0]
                line = line[1:]
            tokens = line.split()            
            if tokens and tokens[0] in '>>':
                rewrite = True if tokens[0] == '>' else False
                if len(tokens) > 2:
                    bufname = tokens[1]
                    if bufname in ed.buffers:
                        buf = ed.buffers[bufname]
                        if rewrite:
                            buf.d(1, buf.nlines()) 
                        else: # append
                            buf.dot = buf.nlines()
                    else:
                        ed.buffers[bufname] = buffer.Buffer(bufname)
                    dest = ed.buffers[bufname] 
                    ed.b(bufname)
                    line = prefix + ' '.join(tokens[2:])
                else:
                    print('? > <buffer name> <command>')
            else:
                dest = display.tty
                line = prefix + line

            # process line with redirect            
            if python_mode:
                if len(line) > 1 and line[0] == ':':
                    with redirect_stdout(dest):
                        process_line(line[1:])
                elif line == ':':
                    python_mode = False
                else:
                    with redirect_stdout(dest):
                        pysh.push(line)
            else: # not python_mode
                if len(line) > 1 and line[0] == '!':
                    with redirect_stdout(dest):
                        pysh.push(line[1:])
                elif line == '!':
                    python_mode = True
                elif pysh.continuation:
                    with redirect_stdout(dest):
                        pysh.push(line)
                else: 
                    with redirect_stdout(dest):
                        process_line(line)
        else: # not command_mode()
            process_line(line)
        prompt = pysh.prompt if python_mode else command_prompt()
        return 
    return _process_line

if __name__ == '__main__':

    class Namespace(object): pass

    app = Namespace()

    app.command_mode = True # False is insert mode
    app.running = True
    app.command_prompt = ':'
    app.input_prompt = ' ' # no prompt, but indent to indicate mode
    app.prompt = app.command_prompt

    def app_process_line(line):
        if app.command_mode:
            print('Executing ' + line)
            if line in ('a','i','c'):  # insert mode commands
                app.command_mode = False
                app.prompt = app.input_prompt
            if line == 'q':
                app.running = False
        else: # app insert mode
            print(' inserting ' + line)
            if line == '.': # exit insert mode
                app.command_mode = True
                app.prompt = app.command_prompt

    app.process_line = app_process_line

    prompt = app.prompt # global initialized above

    process_line = shell(process_line=app.process_line,
                         command_mode=(lambda: app.command_mode),
                         command_prompt=(lambda: app.prompt))

    def main():
        pysh.start()
        app.running = True
        while app.running:
            line = input(prompt)
            process_line(line)

    main()
