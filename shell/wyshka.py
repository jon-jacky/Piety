"""
wyshka.py - shell that alternates between the pysh (python) REPL
            and the command line interface to another application program,
            (such as ed), like this:

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

class Namespace(object): pass

python_mode = False

def wyshka(do_command=(lambda line: None), command_mode=(lambda: True), 
           prompt=(lambda: '')):
    """
    Return a function with one argument (as string, the command line) to 
    send command to Python or the application.  

    This function has three optional keyword arguments with defaults:

    do_command is a callable with one string argument - the command line -
    that executes an application command.  Default does nothing.

    command_mode is a callable with no arguments that returns True
    when the application is in a state where its command interpreter
    can be switched to Python mode.  Default always returns True.

    prompt is a callable with no arguments that returns the application
    prompt string.  Default always returns the empty string.
    """
    def wyshka_do_command(line):
        global python_mode
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
        return (pysh.prompt if python_mode else prompt())
    return wyshka_do_command

# stub application for testing

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

do_command = wyshka(do_command=app.do_command,
                    command_mode=(lambda: app.command_mode),
                    prompt=(lambda: app.prompt))
                                  
def main():
    pysh.start()
    app.running = True
    prompt = (pysh.prompt if python_mode else app.prompt)
    while app.running:
        line = input(prompt)
        prompt = do_command(line)

if __name__ == '__main__':
    main()
