"""
pysh.py - Callable Python shell, based on Python standard library code module
"""

import sys, code

ps1 = '>> '  # first line prompt, named like sys.ps1
ps2 = '.. '  # continuation line prompt, named like sys.ps2
                  
running = True
continuation = False # True when continuation line expected
prompt = ps1

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

def push(line):
    'Push one line to Python interpreter'
    global continuation, prompt
    if line == 'exit()': # DON'T exit from underlying Python session ...
        stop() # ... instead assign running variable, can be used by caller
        continuation = False
    else:
        continuation = pysh.push(line) # True if continuation line expected
    prompt = ps2 if continuation else ps1

def main():
    'Python REPL using home-made pysh shell'
    start()
    print("pysh shell, type any Python statement, exit() to exit")
    while running:
        line = input(prompt)
        push(line)

if __name__ == '__main__':
    main()
