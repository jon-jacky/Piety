# test_ed_s.sh - Same operations as test_ed_s.py but commands not API
#
python -c "from ed import *; ed()" <<'END'
a
ed is an editor based on the classic Unix editor ed.
Again we mention ed.  This is test of ed.
In this line there is no mention of it.
In this line there is a single mention of ed.
And in this last line we mention ed, then ed again, twice altogether.
.
1,$p
p
s/ed/emacs/g
p
s/emacs/vi/
p
1s/ed/emacs/g
p
1s/emacs/vi/
p
1s/emacs/ed/g
1p
2,4s/ed/vi/g
1,$p
2,4s/vi/emacs/
1,$p
q
END
