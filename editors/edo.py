"""
edo.py - ed + wyshka, ed with command interpreter that also provides python
            + samysh, run script from buffer with optional echo and delay
          Also add R command to run Python script from buffer,
          P command to run Python statements in current selection
"""

import ed, pysh, samysh, wyshka

# Define x command so it can also be imported by edsel, eden etc.
# to use with their own do_commands, by calling samysh.add_command.

def X_command(do_command):
    """
    Return function to run script from buffer using do_command,
    with optional echo and delay.
    """
    def X(paramstring):
        """
        Run script from buffer with optional echo and delay, coded in line arg.
        Named x for eXecute, a single letter like other ed command functions.
        paramstring has buffer name, echo, delay, for example 'modes.ed 0 1'
        Buffer name can be abberviated with - , for example 'modes- 0 1'
        Buffer name is required, default echo is True, default delay is 1 sec.
        """
        if ed.command_mode:
            echo, delay = (lambda: True), 1
            params = paramstring.split()
            if len(params) > 1:
                echo = ((lambda: not ed.command_mode)
                        if params[1] in ('0','f','false','F','False')
                        else (lambda: True))
            if len(params) > 2:
                try:
                    delay = float(params[2])
                except ValueError:
                    pass # use default
            bufname = params[0] if len(params) > 0 else ''
            bufname = ed.match_prefix(bufname, ed.buffers)
            if bufname in ed.buffers and bufname != ed.current:
                lines = ed.buffers[bufname].lines[1:] # lines[0] always empty
                samysh.run_script(do_command, lines, echo=echo, delay=delay)
            else:
                print('? buffer name')
    return X

def R(bufname, start, end):
    '(R)un Python script from buffer, lines start through end'
    source = ''.join(ed.buffers[bufname].lines[start:end+1])
    pysh.pysh.runsource(source, filename=bufname)

def P():
        'Run (P)ython code in current selection (point up to dot)'
        # based on eden cut method
        if '@' in ed.buf.mark:
            start = ed.buf.mark['@']
            end = ed.buf.dot
            if start > end:
                start, end = end, start
            end -= 1 # exclude last line, dot (usually) or mark
            if ed.check.range_ok(ed.buf, start, end):
                R(ed.current, start, end)
        else:
            print('? no mark, no region')

def do_command(line):
        """
        Add R command to (R)un Python script from buffer,
        P command to run Python statements in current selection.
        """
        line = line.lstrip()
        paramstring = line[1:].lstrip()
        if line.startswith('R'):
            bufname = paramstring if paramstring else ed.current
            if not bufname in ed.buffers:
                print('? buffer name')
                return
            R(bufname, 1, ed.S()) # always the whole buffer
        elif line.startswith('P'):
            P()
        else:
            ed.do_command(line)

def base_process_line(line):
    'do_command, add P command to run Python script from buffer'
    if ed.command_mode:
        do_command(line)
    else:
        ed.add_line(line)

# Add embedded python interpreter to ed command line.
_process_line = wyshka.shell(process_line=base_process_line,
                            command_mode=(lambda: ed.command_mode),
                            command_prompt=(lambda: ed.prompt))

# Add command to run script from buffer with optional echo and delay.
process_line = samysh.add_command(X_command(_process_line), _process_line)

def startup(*filename, **options):
    ed.startup(*filename, **options)
    wyshka.prompt = ed.prompt

def main(*filename, **options):
    'Top level edo command to invoke from Python REPL or __main__'
    startup(*filename, **options)
    while not ed.quit:
        line = input(wyshka.prompt) # blocks!
        process_line(line)

if __name__ == '__main__':
    filename, options = ed.cmd_options()
    main(*filename, **options)
