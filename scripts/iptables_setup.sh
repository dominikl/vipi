#!/bin/bash
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE 
iptables -t nat -A POSTROUTING -o tun0 -j MASQUERADE

iptables -N CLIENTSLOG
iptables -A INPUT -i wlan0 -s 192.168.12.1/24 -j CLIENTSLOG
iptables -A INPUT -i eth0 -s 192.168.13.1/24 -j CLIENTSLOG
iptables -A CLIENTSLOG -m recent --set --name clients 
iptables -A CLIENTSLOG -m recent --update --rsource --seconds 300 --name clients

iptables -A FORWARD -i tun0 -o wlan0 -d 192.168.12.1/24 -m state --state RELATED,ESTABLISHED -j ACCEPT 
iptables -A FORWARD -i tun0 -o eth0 -d 192.168.13.1/24 -m state --state RELATED,ESTABLISHED -j ACCEPT
iptables -A FORWARD -i wlan0 -o tun0 -s 192.168.12.1/24 -j ACCEPT  
iptables -A FORWARD -i eth0 -o tun0 -s 192.168.13.1/24 -j ACCEPT  

