# sample.sh - test ed.py command mode and input mode  with example from ed.md
#              additional commands confirm file got written and show its contents
python -c "import ed; ed.main()" <<'END'
e test.txt
a
ed() enters ed command mode.  By default, there is no command prompt.
'e <name>' loads the named file into the current buffer.
'a' enters ed input mode and appends the text after the current line.
'w' writes the buffer contents back to the file
'q' quits ed command mode.
To quit input mode, type a period by itself at the start of a line.
.
w
B test.txt
1,$p
q
END
echo ""
echo "Remove test.txt before running this again, to get the same results"