#!/usr/bin/env bash

#
# Script que permite la instalacion de Docker
#
# AUTHOR: John Sanabria - john.sanabria@correounivalle.edu.co
# DATE: 2020-04-29
#

sudo apt-get update
sudo apt update && sudo apt install python-pip -y
export LC_ALL=C
sudo pip install --upgrade pip 
pip install flask
