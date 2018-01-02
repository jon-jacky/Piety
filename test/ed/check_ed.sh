set -x
python3 -m ed < $1.ed > $1.ed.newlog 2>/dev/null
diff $1.ed.newlog $1.ed.log
