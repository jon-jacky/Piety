# test_ed_kmty3.sh - test ed.py command mode with k m t y commands
#              additional commands confirm file got written and show its contents
# We do not write out line20.txt, so we can run this test again w/same result.
python3 -c "import ed; ed.main()" <<'END'
e line20.txt
3ka
5kb
7kc
9kd
15ke
18kf
!ed.buf.mark
'a,'bm12
!ed.buf.mark
'a
'b
,p
'a,'bt0
'a,'bt$
!ed.buf.mark
,p
'a
'b
'c
'd
'e
'f
!ed.deleted
!ed.deleted_mark
16y
!ed.buf.mark
,p
END

