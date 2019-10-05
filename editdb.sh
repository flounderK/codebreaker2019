#!/bin/sh 

adb root > /dev/null
adb shell sqlite3 -interactive /data/data/com.badguy.terrortime/databases/clientDB.db 

