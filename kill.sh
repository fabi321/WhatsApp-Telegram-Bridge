#!/bin/sh
a=`grep "^\[ERROR\]" log.txt`
if [ $? -eq 0 ]; then
    for j in `cat log.pid`
    do
      kill -9 ${j}
    done
    #. ./UploadToTG.sh
    rm log.pid
    rm log.txt
    . ./run.sh
fi
