#!/bin/bash
PREV_PWD=$PWD
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $DIR
./kill.sh
./run.sh
cd $PREV_PWD
