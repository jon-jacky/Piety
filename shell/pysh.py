"""
pysh.py - Callable Python shell, based on Python standard library code module
"""

import sys, code

# pysh exit() is managed by pysh itself, must not exit top-level Python session

running = True
more = False # True when continuation line expected
                  
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
    'Execute one line with the Python interpreter'
    global more
    if command == 'exit()':  # DON'T exit from underlying Python session
        stop()    # instead assign running variable, can be used by caller
        return False # False means command is complete
    more = pysh.push(command) # True if continuation line expected
    # pysh.resetbuffer() # do we ever need to call this?

def main():
    'Python REPL using home-made pysh shell'
    start()
    print("pysh shell, type any Python statement, exit() to exit")
    while running:
        command = input('>> ' if not more else '.. ') # blocking input
        do_command(command)

if __name__ == '__main__':
    main()
