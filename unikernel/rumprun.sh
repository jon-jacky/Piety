# $1 is the full name of the unikernel file, for example echo.bin (not just echo)
rumprun qemu -i    -b /Users/jon/rumprun-packages/python/images/python.iso,/python/lib/python3.4 -b /Users/jon/rumprun-packages/python/images/stubetc.iso,/etc   -e PYTHONHOME=/python $1
