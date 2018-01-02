set -x
python3 -m edo < $1.edo > $1.edo.newlog 2>/dev/null
diff $1.edo.newlog $1.edo.log
