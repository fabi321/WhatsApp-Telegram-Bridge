#!/bin/sh

# TODO: grep for the Bad Error keyword

# to kill the PID
for i in `ls *.pid`
do
    for j in `cat ${i}`
    do
        kill -9 ${j}
    done
    rm ${i}
done

