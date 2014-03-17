# test_ed_urc.sh - Same operations as test_ed_urc.py but commands not API
#                    BUT don't print buffer after every command, just at end
python -c "from ed import *; ed()" <<'END'
b new.txt
n
r test_cmd.py
1,$p
10l
r README.md.txt
p
c
### This is the changed line ###
.
e
1,$p
27l
.,$c
### This line replaces all that follows ###
.
1,$p
q
END

