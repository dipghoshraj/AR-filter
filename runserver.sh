#!/usr/bin/env bash

echo "start pull"
git pull origin master
echo "pull complete"

echo "Stop existing pools"
sudo fuser -k 5000/tcp

echo "Start new pools"
gunicorn --certfile=/etc/letsencrypt/live/ar.dliticx.click/fullchain.pem --keyfile=/etc/letsencrypt/live/ar.dliticx.click/privkey.pem --bind 0.0.0.0:5000 wsgi:app --reload