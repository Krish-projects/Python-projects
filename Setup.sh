#!/bin/bash

cd ~/files
sudo  systemctl stop capture.service
python3 GUI.py
