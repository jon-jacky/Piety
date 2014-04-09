# test_ed_r.sh - Same operations as test_ed_r.py but commands not API
#
python -c "from ed import *; ed()" <<'END'
a
Line 0
Line 1
Line 2
.
1,$p
b
r
101r rtest0.txt
r rtest0.txt
1,$p
1r rtest1.txt
1,$p
q
END
