#!/bin/bash
PREV_PWD=$PWD
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $DIR
for j in `cat log.pid`
do
  kill -9 ${j}
done
rm log.pid
rm log.txt
cd $PREV_PWD
