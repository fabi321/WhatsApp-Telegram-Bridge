#!/bin/sh
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
     . ./kill.sh
  fi
done
done
