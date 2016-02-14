# sample.py   test edsel.py command mode and input mode  with example from ed.md
#               to run: python3 -i sample.py 

import edsel
edsel.init_session(h=16) # assumes window with at least 24 lines
edsel.cmd('e test.txt')
edsel.cmd('a')
edsel.cmd('ed() enters ed command mode.  By default, there is no command prompt.')
edsel.cmd("'e <name>' loads the named file into the current buffer.")
edsel.cmd("'a' enters ed input mode and appends the text after the current line.")
edsel.cmd("'w' writes the buffer contents back to the file")
edsel.cmd("'q' quits ed command mode.")
edsel.cmd("To quit input mode, type a period by itself at the start of a line.")
edsel.cmd('.')
edsel.cmd('w')
edsel.cmd('B test.txt')
edsel.cmd('1,$p')
edsel.cmd('q')
print("")
print("Remove test.txt before running this again, to get the same results")
