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

interpreter = code.InteractiveConsole(locals=main_globals)

def push(line):
    'Push one line to Python code.InteractiveConsole interpreter'
    global continuation, prompt
    if line == 'exit()': # DON'T exit from underlying Python session ...
        stop() # ... instead assign running variable, can be used by caller
        continuation = False
    else:
        continuation = interpreter.push(line) # True if continuation line expected
    prompt = ps2 if continuation else ps1

# Append extra empty line, otherwise push doesn't always execute line properly.
# We got the idea to append a blank line after reading source in standard
# library codeop.py, the comment that begins 'Compile three times: ...'

def pushlines(lines):
    'Run a sequence of lines in the Python InteractiveConsole using push'
    for line in lines + ['\n']:
        push(line.rstrip('\n')) # remove any terminal \n from line

# execlines does not behave the same as pushlines; it uses builtin exec
# not InteractiveConsole.  Values of expressions are not printed by default.
# execlines second argument is needed to update variables seen by pysh.

def execlines(lines):
    'Run a sequence of lines in the Python interpreter using builtin exec'
    exec(''.join(lines), main_globals)

def main():
    'Python REPL using home-made pysh shell'
    start()
    print("pysh shell, type any Python statement, exit() to exit")
    while running:
        line = input(prompt)
        push(line)

if __name__ == '__main__':
    main()
