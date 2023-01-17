#!/bin/bash

#give permission for everything in the express-app directory
sudo chmod -R 777 /home/ubuntu/pop-API

#Creating an .env file from .env.example
cd /home/ubuntu/pop-API/backend/core
sudo npm install aws-sdk fs os
sudo cp .env.example .env

#navigate into our working directory where we have all our github files
cd /home/ubuntu/pop-API

#source env/bin/activate
#pip install -r requirements.txt

#Collecting enviroment variables
sudo node ssmToenv.js