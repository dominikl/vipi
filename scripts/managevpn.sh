#!/bin/bash

server1=Germany-Frankfurt-UDP
server2=Netherlands-Amsterdam-UDP
server3=Russia-Moscow-UDP
server4=United_Kingdom-Maidenhead-UDP

openvpncmd="/usr/sbin/openvpn"
openvpncfg="/etc/openvpn"
logfile="/var/log/openvpn.log"

if [[ ! "$1" ]]
then
    echo "0 - disconnected"
    echo "1 - $server1"
    echo "2 - $server2"
    echo "3 - $server3"
    echo "4 - $server4"
    exit 0
fi

if [[ "$1" == "info" ]]
then
    if [[ "$2" == 1 ]]
    then
        echo $server1
    fi

    if [[ "$2" == 2 ]]
    then
        echo $server2
    fi

    if [[ "$2" == 3 ]]
    then
        echo $server3
    fi

    if [[ "$2" == 4 ]]
    then
        echo $server4
    fi
    exit 0
fi

if [[ "$1" == "status" ]]
then
    pid=`pgrep openvpn`
    if [[ $pid ]]
    then
        param=`ps -o args $pid`
	param=${param#*openvpn/}
	param=${param%.*}

        if [[ $param == $server1 ]]
        then
            echo 1
            exit 0
        fi

        if [[ $param == $server2 ]]
        then
            echo 2
            exit 0
        fi

        if [[ $param == $server3 ]]
        then
            echo 3
            exit 0
        fi

        if [[ $param == $server4 ]]
        then
            echo 4
            exit 0
        fi
    else
        echo 0
        exit 0
    fi
fi

if [[ "$1" == "disconnect" ]]
then
    pid=`pgrep openvpn`
    if [[ $pid ]]
    then
        kill $pid
    fi

    exit 0
fi

if [[ "$1" == "connect" ]]
then
    pid=`pgrep openvpn`
    if [[ $pid ]]
    then
        kill $pid
    fi

    if [[ "$2" == 1 ]]
    then
        $openvpncmd --log-append $logfile --config $openvpncfg/$server1.ovpn & disown
    fi

    if [[ "$2" == 2 ]]
    then
        $openvpncmd --log-append $logfile --config $openvpncfg/$server2.ovpn & disown
    fi

    if [[ "$2" == 3 ]]
    then
        $openvpncmd --log-append $logfile --config $openvpncfg/$server3.ovpn & disown
    fi

    if [[ "$2" == 4 ]]
    then
        $openvpncmd --log-append $logfile --config $openvpncfg/$server4.ovpn & disown
    fi

    exit 0
fi
