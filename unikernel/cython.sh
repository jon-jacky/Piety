# $1 is basename of file, for example echo in echo.py.  This command creates echo.c 
cython3.4 --embed -v -3 -Werror -o $1.c $1.py
