#!/bin/bash

#download python,node and npm---
curl -sL https://deb.nodesource.com/setup_16.x | sudo -E bash -
sudo apt-get install -y nodejs
sudo apt-get install -y python3 python-dev python3-pip
#sudo npm i -g pm2@latest

#create our working directory if it doesnt exist
DIR="/home/ubuntu/pop-API"
if [ -d "$DIR" ]; then
  echo "${DIR} exists"
else
  echo "Creating ${DIR} directory"
  sudo mkdir ${DIR}
fi
