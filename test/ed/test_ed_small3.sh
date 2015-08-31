# test_ed_small.sh - Same operations as test_ed_small.py but commands not API
#
python3 -c "import ed; ed.main()" <<'END'
B test_ed_small.txt
i
Line i
.
1,$p
d
1,$p
a
Line a
.
1,$p
d
1,$p
i
Line i
.
1,$p
1l
a
Line a
.
1,$p
w
d
i
Line ii
.
w test_ed_small_2.txt
d
b new.txt
a
Line 1
.
a
Line 2
.
1,$p
c
Changed line 2
.
1c
Changed line 1
.
1,$p
q
END
echo ""
echo "Remove test_ed_small.txt and test_ed_small_2.txt"
echo "before running this script again, to obtain the same result"
