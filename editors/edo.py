"""
edo.py - ed + wyshka, ed with command interpreter that also provides python
            + samysh, run script from buffer with optional echo and delay
          Also add R command to run Python script from buffer,
          P command to run Python statements in current selection
          bimport() and breload() functions to import, reload from buffers
"""

import ed, parse, check, pysh, samysh, wyshka, bufimport, shellcmd
text = ed.text # so we can use it without ed prefix
bimport, breload, sh = bufimport.bimport, bufimport.breload, shellcmd.sh

# Define x command so it can also be imported by edda, edsel etc.
# to use with their own do_commands, by calling samysh.add_command.

def X_command(do_command):
    """
    Return function named X to run script from buffer using do_command,
    with optional echo and delay.
    """
    def X(paramstring):
        """
        Run script from buffer with optional echo and delay, coded in line arg.
        Named X for eXecute, a single letter like other ed command functions.
        paramstring has buffer name, echo, delay, for example 'modes.ed 0 1'
        Buffer name can be abberviated with - , for example 'modes- 0 1'
        Buffer name is required, default echo is True, default delay is 1 sec.
        """
        if ed.command_mode:
            bufname, echo, delay = samysh.params(paramstring)
            bufname = ed.match_prefix(bufname, text.buffers)
            if bufname in text.buffers and bufname != text.current:
                lines = text.lines(bufname)
                samysh.run_script(do_command, lines, echo=echo, delay=delay)
            else:                
                print('? buffer name')
    return X

def P(*args):
    'Run Python statements in addressed lines using push'
    valid, start, end, _, _ = check.irange(text.buf, args)
    if valid: # includes start <= end, maybe not so for mark and dot
        pysh.pushlines(text.buf.lines[start:end+1])
        print('%s, ran lines %d..%d using push' % (text.current, start, end))

def R(*args):
    'Run Python statements in addressed lines using exec'
    valid, start, end, _, _ = check.irange(text.buf, args)
    if valid: # includes start <= end, maybe not so for mark and dot
        pysh.execlines(text.buf.lines[start:end+1])
        print('%s, ran lines %d..%d using exec' % (text.current, start, end))

parse.ed_cmds += 'PR' # so parse.command() recognizes new commands

def do_command(line):
        'Add P and R commands to run Python statements'
        results = parse.command(text.buf, line)
        if results:
            cmd_name, args = results
        else:
            return # parse already printed error message
        if cmd_name == 'R':
            R(*args)
        elif cmd_name == 'P':
            P(*args)
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
