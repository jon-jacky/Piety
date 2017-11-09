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

# FIXME: parameterize by application and console
def do_command(line):
    'Send command to Python or app, manage prompt'
    global python_mode
    if app.command_mode:
        if python_mode:
            if len(line) > 1 and line[0] == ':':
                app.do_command(line[1:])
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
                app.do_command(line)        
    else: # not app.command_mode
        app.do_command(line)
    return (pysh.prompt if python_mode else app.prompt)

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

def main():
    pysh.start()
    app.running = True
    prompt = (pysh.prompt if python_mode else app.prompt)
    while app.running:
        line = input(prompt)
        prompt = do_command(line)

if __name__ == '__main__':
    main()
