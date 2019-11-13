#!/bin/sh
cd $PWD/WhatsApp-Telegram-Bridge/
. ./venv/bin/activate
WAT_CONF=config.conf python3 watbridge.py >> log.txt 2>&1 & echo $! >> log.pid
