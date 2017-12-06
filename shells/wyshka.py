"""
wyshka.py - Shell that can alternate between pysh (Python)
            and the command line interface to another application program,
            such as ed.  You can use Python without leaving the application.

It works like this:

 :<command>       execute ed <command>
 :!<statement>    push Python <statement> to pysh, return to ed command mode
 .. <statement>   push Python continuation line <statement> to pysh
 :!               switch to Python mode

 and Python mode:

 >> <statement>   push Python <statement> to pysh
 .. <statment>    push Python continuation line <statement> to pysh
 >>:<command>     execute ed <command>, return to pysh interpreter
 >>:              switch to ed command mode

"""

import pysh

def wyshka(do_command=(lambda line: None), command_mode=(lambda: True), 
           command_prompt=(lambda: '')):
    """
    Return a function with one argument (a string, the command line) that
    sends a command either to Python or to another application.  

    This function has three optional keyword arguments with defaults:

    do_command is a callable with one string argument - the command line -
    that executes an application command.  Default does nothing.

    command_mode is a callable with no arguments that returns True
    when the application is in a state where its command interpreter
    can be replaced by Python.  Default always returns True.

    command_prompt is a callable with no arguments that returns the
    application prompt string, which might depend on application
    state.  Default always returns the empty string.
    """
    def specialized_do_command(line):
        global python_mode, prompt
        if command_mode():
            if python_mode:
                if len(line) > 1 and line[0] == ':':
                    do_command(line[1:])
                elif line == ':':
                    python_mode = False
                else:
                    pysh.push(line)
            else: # not python_mode
                if len(line) > 1 and line[0] == '!':
                    pysh.push(line[1:])
                elif line == '!':
                    python_mode = True
                elif pysh.continuation:
                    pysh.push(line)
                else: 
                    do_command(line)        
        else: # not command_mode()
            do_command(line)
        prompt = pysh.prompt if python_mode else command_prompt()
        return 
    return specialized_do_command

# stub application for testing

class Namespace(object): pass

app = Namespace()

app.command_mode = True # False is insert mode
app.running = True
app.ps1 = ':' # command mode prompt
app.ps2 = ' '  # insert mode, no prompt, but indent to indicate mode
app.prompt = app.ps1

def app_do_command(line):
    if app.command_mode:
        print('Executing ' + line)
        if line in ('a','i','c'):  # insert mode commands
            app.command_mode = False
            app.prompt = app.ps2
        if line == 'q':
            app.running = False
    else: # app insert mode
        print(' inserting ' + line)
        if line == '.': # exit insert mode
            app.command_mode = True
            app.prompt = app.ps1

app.do_command = app_do_command

# end stub application

# globals used by wyshka
python_mode = False
prompt = app.prompt

do_command = wyshka(do_command=app.do_command,
                    command_mode=(lambda: app.command_mode),
                    command_prompt=(lambda: app.prompt))
                                  
def main():
    pysh.start()
    app.running = True
    while app.running:
        line = input(prompt)
        do_command(line)

if __name__ == '__main__':
    main()
