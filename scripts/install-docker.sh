#!/usr/bin/env bash
#
# Script que permite la instalacion de Docker
#
# AUTHOR: John Sanabria - john.sanabria@correounivalle.edu.co
# DATE: 2020-04-29
#


sudo apt-get -y --force-yes install docker.io
sudo usermod -aG docker vagrant

