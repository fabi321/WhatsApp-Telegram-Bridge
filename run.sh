#!/bin/bash
PREV_PWD=$PWD
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $DIR
. ./venv/bin/activate
WAT_CONF=config.conf python3 watbridge.py >> log.txt 2>&1 & echo $! >> log.pid
cd $PREV_PWD
