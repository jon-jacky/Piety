# sample.sh - test ed.py command mode and input mode  with example from ed.md
#              additional commands confirm file got written and show its contents
python -c "from ed import *; ed()" <<'END'
B test.txt
a
ed() enters ed command mode, with the : command  prompt.
'B <name>' creates a new buffer and loads the named file
'a' enters ed input mode and appends the text after the current line.
'w' writes the buffer contents back to the file
'q' quits ed command mode.
To quit input mode, type a period by itself at the start of a line.
.
w
D
B test.txt
1,$p
q
END
echo ""
echo "Remove test.txt before running this again, to get the same results"