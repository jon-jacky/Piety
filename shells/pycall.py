"""
pycall.py - Callable Python interpreter using standard library code module.
"""

import sys, code

main_globals = sys.modules['__main__'].__dict__

interpreter = code.InteractiveConsole(locals=main_globals)

def pycall(cmd):
    """
    Push cmd, a line of text,  to Python code.InteractiveConsole interpreter
    Return True if continuation line expected, False otherwise.
    """
    continuation = interpreter.push(cmd) # True if continuation line expected
    return continuation

def main():
    print("Home-made Python REPL. Type exit() to exit")

    ps1 = '>> '  # first line prompt, different from CPython >>>
    ps2 = '.. '  # continuation line prompt

    continuation = False # True when continuation line expected

    while True:
        prompt = ps2 if continuation else ps1
        cmd = input(prompt)  # python -i makes readline editing work here.
        if cmd == 'exit()':  # Trap here, do *not* exit calling Python session.
            break
        continuation = pycall(cmd)

if __name__ == '__main__':
    main()
