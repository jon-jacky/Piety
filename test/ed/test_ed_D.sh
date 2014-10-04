# test_ed_D.sh - Same operations as test_ed_D.py but commands not API
#
python -c "import ed; ed.main()" <<'END'
B new.txt
i
Here is a line
.
n
D
X
n
B new1.txt
i
Here is a line
.
n
w
D
n
B new2.txt
i 
Here is a line
.
n
w
b main
n
D new2.txt
n
q
END
echo ""
echo "Remove new1.txt, new2.txt before running script again to obtain same results"
