"""
pysh.py - Callable Python shell, based on Python standard library code module

"""

import sys, code

# pysh exit() is managed by pysh itself, must not exit top-level Python session

running = True
                  
def start():
    'Start or resume pysh REPL'
    global running
    running = True

def stop():
    'Stop pysh REPL'
    global running
    running = False

main_globals = sys.modules['__main__'].__dict__

pysh = code.InteractiveConsole(locals=main_globals)

def do_command(command):
    if command == 'exit()':  # DON'T exit from underlying Python session
        stop()    # instead assign running variable, can be used by caller
        return
    pysh.push(command)    
    pysh.resetbuffer()

def main():
    'Python REPL using home-made pysh shell'
    start()
    print("pysh shell, type any Python statement, exit() to exit")
    while running:
        command = input('>> ')
        do_command(command)

if __name__ == '__main__':
    main()
