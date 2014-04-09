# test_ed.sh - Same operations as test_ed.py but commands not API calls here
#
python -c "from ed import *; ed()" <<'END'
B 42
B test_ed.txt
B ed.py.txt
n
b
1,6p
7l
l
l
l
l
p
100p
p
.=
=
b
n
b test_ed.txt
b
n
D foo.txt
D ed.py.txt
n
i
Line 1
Line 2
Line 3
.
p
1,$p
a
Line A
Line B
Line C
.
p
1,$p
1i
Line a
Line b
Line c
.
p
1,$p
4l
i
Line i
Line ii
Line iii
.
p
1,$p
6a
Line I
Line II
Line III
.
p
1,$p
w
13l
p
d
p
.,$d
p
1,$p
q
END
echo ""
echo "Remove test_ed.txt before running this script again, to obtain the same result"
