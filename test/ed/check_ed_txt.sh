set -x
rm $1.txt
./check_ed.sh $1
diff $1.txt $1.txt.save
