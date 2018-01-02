set -x
./check_ed_txt.sh sample
./check_ed_txt.sh test_ed
./check_edo_txt.sh kmty3
rm small2.txt
./check_ed_txt.sh small
diff small2.txt small2.txt.save
rm D1.txt
./check_ed_txt.sh D
diff D1.txt D1.txt.save
./check_ed.sh BnbpD
./check_ed_txt.sh ef
./check_ed.sh pattern
./check_ed.sh r
./check_ed.sh s
./check_ed.sh urc

