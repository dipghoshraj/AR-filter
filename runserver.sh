#!/usr/bin/env bash

echo "start pull"
git pull origin master
echo "pull complete"

echo "Stop existing pools"
sudo fuser -k 5000/tcp
echo "server is running now"