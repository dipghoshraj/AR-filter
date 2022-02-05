#!/usr/bin/env bash

echo "start pull"
git pull origin master
echo "pull complete"

echo "Stop existing pools"
sudo fuser -k 5000/tcp

echo "Start new pools"
gunicorn --certfile=/home/ubuntu/AR-filterfullchain.pem --keyfile=/home/ubuntu/AR-filter/privkey.pem --bind 0.0.0.0:5000 wsgi:app --reload