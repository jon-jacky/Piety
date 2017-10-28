"""
edo.py - Run *ed.py* line editor.  Use *console* module
  instead of Python builtin *input()* to collect and edit
  input lines.  Contrast to *ed.py* *main* function and *etty.py*.
  
 Provides command interpreter with ed mode:

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

import ed, pysh, console as con

python_mode = False

def do_command(line):
    'Send command to Python or ed, manage prompts and keymaps'
    global python_mode
    if python_mode and ed.command_mode:
        if len(line) > 1 and line[0] == ':': # FIXME use slice w/o guard
            ed.do_command(line[1:])
            console.prompt = pysh.ps1 if ed.command_mode else ed.ps2
            console.keymap = (con.command_keymap if ed.command_mode 
                              else con.insert_keymap)
        elif line == ':':
            python_mode = False
            console.prompt = ed.ps1
        else:
            pysh.push(line)
            console.prompt = pysh.ps2 if pysh.continuation else pysh.ps1
    elif not python_mode and ed.command_mode:
        if len(line) > 1 and line[0] == '!':
            pysh.push(line[1:])
            console.prompt = pysh.ps2 if pysh.continuation else ed.ps1
        elif line == '!':
            python_mode = True
            console.prompt = pysh.ps1
        elif pysh.continuation:
            pysh.push(line)
            console.prompt = pysh.ps2 if pysh.continuation else ed.ps1
        else: 
            ed.do_command(line)        
            console.prompt = ed.ps1 if ed.command_mode else ed.ps2
            console.keymap = (con.command_keymap if ed.command_mode 
                              else con.insert_keymap)
    else: # ed input mode
        ed.do_command(line)        
        console.prompt = ed.ps1 if ed.command_mode else ed.ps2
        console.keymap = (con.command_keymap if ed.command_mode 
                          else con.insert_keymap)

console = con.Console(prompt=ed.ps1, do_command=do_command,
                      stopped=(lambda command: ed.quit))

def main():
    ed.startup()
    console.run()

if __name__ == '__main__':
    main()
