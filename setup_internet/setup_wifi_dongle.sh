#!/bin/bash

# sets up the RTL8188FU driver for Linux kernel 4.15.x ~ 6.0.x on debian based images
# See https://github.com/kelebek333/rtl8188fu for more instructions

echo "Install linux headers to build the wifi drivers..."
sudo apt-get install build-essential git dkms linux-headers-$(uname -r)

echo "Done installing all the necessary packages"

echo "Cloning the driver repository"
git clone https://github.com/kelebek333/rtl8188fu

echo "Done cloning the driver repo"

echo "Installing the driver. This will take a min..."
sudo dkms install ./rtl8188fu

echo "Done installing the driver."

echo "Adding to lib firmware"
sudo cp ./rtl8188fu/firmware/rtl8188fufw.bin /lib/firmware/rtlwifi/
echo "Done"

echo "Setting configs for the driver..."
sudo mkdir -p /etc/modprobe.d/

sudo touch /etc/modprobe.d/rtl8188fu.conf

echo "options rtl8188fu rtw_power_mgnt=0 rtw_enusbss=0" | sudo tee /etc/modprobe.d/rtl8188fu.conf

sudo mkdir -p /etc/NetworkManager/conf.d/

sudo touch /etc/NetworkManager/conf.d/disable-random-mac.conf

echo -e "[device]\nwifi.scan-rand-mac-address=no" | sudo tee /etc/NetworkManager/conf.d/disable-random-mac.conf

echo "Done setting configs. Setup should now be complete."

echo "Checking if the driver is there... Should see some results from the grep"
ip a | grep "wlan"
if ip a | grep "wlan" ; then
    echo "Success it looks like there is a wifi driver now"
else
    echo "No wifi drivers found I guess. Try following https://elinux.org/EBC_Exercise_06_Setting_Up_Wifi or rebooting the machine now and checking again"
fi
