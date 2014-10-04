# test_ef.sh - Test f e E commands
#
python -c "import ed; ed.main()" <<'END'
f
e
f ed.py.txt
e
n
p
a
Here is a new line at the end
.
n
e
E
0
1
n
i
Here is a new line at the start
.
1,3p 
w ed.py.txt.1
f
e
q
END
