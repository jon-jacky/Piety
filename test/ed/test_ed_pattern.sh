# test_ed_pattern.sh - Same fcns as test_ed_pattern.py but commands not API
#
python -c "from ed import *; ed()" <<'END'
B ed.py.txt
/text/l
1l
/text/l
b
/text/l
b
/text/l
b
/text/l
b
?text?l
b
?text?l
b
?text?l
b
//l
1l
//l
b
//l
b
//l
b
//l
b
??l
b
??l
b
??l
b
??l
b
q
END