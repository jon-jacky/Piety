# sample_read.sh - read and display the contents created by sample.py
python -c "from ed import *; ed()" <<END
B test.txt
0,$p
END
