#!/bin/bash

echo "Installing pip..."
sudo apt install python3-pip
echo "Done ^.^"

echo "Installing DLIB deb packages..."
sudo apt-get install build-essential cmake pkg-config
sudo apt-get install libx11-dev libatlas-base-dev
sudo apt-get install libgtk-3-dev libboost-python-dev
echo "Done :)"

echo "Pip install the python packages..."
pip3 install scipy
pip3 install imutils
pip3 install numpy
pip3 install dlib # Needs other packages
pip3 install opencv-python
echo "Yippee it's done!" 

