#!/bin/sh

if [ $# -eq 0 ];then
	echo "Usage: $0 <file.db>"
	exit 1
fi
adb root > /dev/null
adb push $1 /data/data/com.badguy.terrortime/databases/clientDB.db
OWNING_USER=$(adb shell stat -c '%U' /data/data/com.badguy.terrortime/databases/)
OWNING_GROUP=$(adb shell stat -c '%G' /data/data/com.badguy.terrortime/databases/)
adb shell chown $OWNING_USER:$OWNING_GROUP /data/data/com.badguy.terrortime/databases/clientDB.db

