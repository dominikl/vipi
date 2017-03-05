# vipi
Turn your Raspberry PI 3 into a Wifi VPN Gateway

This Ansible playbook will set up a Raspberry PI 3 as Wifi access point routing all the traffic through a VPN connection.
As default it sets up four VPN configurations using [ivacy](https://billing.ivacy.com/page/22007), but it should be straightforward
to change the openvpn configurations to match your VPN provider.

It also installs:

* A script to manage the VPN connections

![ViPi Commandline Interface](/screenshot2.png "ViPi Commandline Interface")

* A simple web Interface (optional)

![ViPi Web Interface](/screenshot.png "ViPi Web Interface")

* A script which enables you to connect a "hardware interface" (breadboard) with
one power led and button, four leds and buttons to handle the VPN connections. (optional)

![ViPi Breadboard](/vipi_bb.png "ViPi Breadboard")

## Setup your Raspberry

* Get [Raspbian Lite](https://www.raspberrypi.org/downloads/raspbian/) and
follow the [Installation guide](https://www.raspberrypi.org/documentation/installation/installing-images/README.md)
* Mount the boot partition of the Raspbian sd card and add an empty file with name ssh: ```touch ssh```. Umount sd card again.
Put it into your Raspberry PI, plugin the LAN cable and start it up.
* Check which IP your Raspberry PI was assigned to, connect via ssh (username: pi, password: raspberry) and run ```sudo raspi-config```
Enlarge the file system (in Advanced options)

## Enable password less root access (you should disable root access later again!)
* Copy your ssh key: ```ssh-copy-id pi@[RASPI IP]```
* SSH into your Raspiberry PI: ```ssh pi@[RASPI IP]```
* Change to root ```sudo su```
* Copy the key ```mkdir /root/.ssh``` ```cp /home/pi/.ssh/authorized_keys /root/.ssh/``` ```chown root:root /root/.ssh/authorized_keys```

## Get Ansible
* [Ansible](https://www.ansible.com/)

## Clone this repository (on your local machine)
* ```git clone https://github.com/dominikl/vipi.git```

## Install
* CD into install directory
* Change the IP address in the [hosts](install/hosts) file to your Raspberry PI's IP address
* Update the configuration in [all](install/group_vars/all) file to match your requirements
* Kick off the automatic installation: ```ansible-playbook -i hosts setup.yml```
