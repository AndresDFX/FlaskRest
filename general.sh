#!/usr/bin/env bash

sudo apt-get update
sudo apt update && sudo apt install python-pip -y
export LC_ALL=C
sudo pip install --upgrade pip 
pip install flask
