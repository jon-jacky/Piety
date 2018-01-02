set -x

rm small2.txt D1.txt
for script in sample test_ed small D ef
do 
 ./check_ed_txt.sh $script
done
diff small2.txt small2.txt.save
diff D1.txt D1.txt.save

./check_edo_txt.sh kmty3

for script in BnbpD pattern r s urc
do 
 ./check_ed.sh $script
done
