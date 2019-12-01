#!/bin/bash
PREV_PWD=$PWD
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $DIR
while :
do
for PID in `cat log.pid`
do
  if ps -p $PID > /dev/null
   then
     echo "$PID is running"
     # Do something knowing the pid exists,
     # i.e. the process with $PID is
     # running
     a=`grep "^\[ERROR\]" log.txt`
     if [ $? -eq 0 ]; then
       sh kill.sh
       sh run.sh
     fi
  fi
done
sleep 10
done
cd $PREV_PWD
