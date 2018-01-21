#!/bin/sh
    for j in `cat log.pid`
    do
      kill -9 ${j}
    done
    sh UploadToTG.sh
    rm log.pid
    rm log.txt
