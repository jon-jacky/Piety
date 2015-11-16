# gcc cross-compile for python on unikernel, via cpython.  $1 is basename, echo in echo.c
x86_64-rumprun-netbsd-gcc $1.c -o $1 -I/Users/jon/rumprun-packages/python/build/pythondist/include/python3.4m  -L/Users/jon/rumprun-packages/python/build/pythondist/lib -lpython3.4m -lutil  -lm -lz -lssl -lcrypto
