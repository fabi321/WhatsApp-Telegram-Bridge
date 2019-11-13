#!/bin/sh
    for j in `cat log.pid`
    do
      kill -9 ${j}
    done
    rm log.pid
    rm log.txt
