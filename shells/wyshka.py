"""
wyshka.py - Shell that can alternate between pysh (Python)
            and the command line interface to another application program,
            such as ed.  You can use Python without leaving the application.
            Can also redirect output to text buffer, rewrite or append
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

            # check command line for redirect, prepare destination
            # allow any amount of whitespace around > and >> 
            if line.lstrip().startswith('>>'):
                redirect, rewrite = True, False
                _, _, line = line.lstrip().partition('>>')
            elif line.lstrip().startswith('>'):
                redirect, rewrite = True, True
                _, _, line = line.lstrip().partition('>')              
            else:
                redirect = False
            if redirect:
                bufname, _, line = line.lstrip().partition(' ')                
                # if bufname and/or line are missing now line is ''
                if not line:
                    print('? bufname command')
                    return 
                if bufname in ed.buffers:
                    buf = ed.buffers[bufname]
                    if rewrite:
                        buf.d(1, buf.nlines()) 
                    else: # append
                        buf.dot = buf.nlines()
                else:
                    ed.buffers[bufname] = buffer.Buffer(bufname)
                dest = ed.buffers[bufname] 
                # do not switch current buffer to dest until after command
            else:
                dest = display.tty

            # process command line, with possible redirect
            # allow whitespace before but not after ! and :
            if python_mode:
                if line.lstrip() == ':':
                    python_mode = False
                elif line.lstrip().startswith(':'):
                    with redirect_stdout(dest):
                        process_line(line.lstrip()[1:])
                else:
                    with redirect_stdout(dest):
                        pysh.push(line)
            else: # not python_mode
                if line.lstrip() == '!':
                    python_mode = True
                elif line.lstrip().startswith('!'):
                    with redirect_stdout(dest):
                        pysh.push(line.lstrip()[1:])
                elif pysh.continuation:
                    with redirect_stdout(dest):
                        pysh.push(line)
                else: 
                    with redirect_stdout(dest):
                        process_line(line)
            # now switch current buffer 
            if redirect:
                ed.b(bufname)

        else: # not command_mode()
            process_line(line)

        prompt = pysh.prompt if python_mode else command_prompt()
        return 
    return _process_line

# Test

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
