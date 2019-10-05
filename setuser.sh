#!/bin/sh 

if [ $# -eq 0 ]; then 
	echo "Usage: $0 <user>"
	echo "E.g. $0 hannah"
	exit 1
fi

adb root > /dev/null 
adb shell sqlite3 -interactive /data/data/com.badguy.terrortime/databases/clientDB.db -cmd "update\ Clients\ set\ xname\ =\ \'$1--vhost-385@terrortime.app\'\;\ select\ xname\ from\ Clients\; .quit"
