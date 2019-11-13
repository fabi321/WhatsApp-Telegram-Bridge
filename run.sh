#!/bin/sh
cd $PWD/WhatsApp-Telegram-Bridge/
WAT_CONF=config.conf python3 watbridge.py >> log.txt 2>&1 & echo $! >> log.pid
