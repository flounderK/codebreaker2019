#!/bin/sh


adb root > /dev/null
adb shell am start -n com.badguy.terrortime/com.badguy.terrortime.LoginActivity
if [ $# -eq 1 ]; then
	sleep 2
	nohup adb logcat --pid=$(adb shell pgrep terror) \*:D > $1 & disown
fi
adb shell input text "roberto--vhost-385@terrortime.app"
adb shell input keyevent 61
adb shell input text "412270"
adb shell input keyevent 61
adb shell input keyevent 66

