#!/bin/sh 
rm heapdump 2> /dev/null
adb root > /dev/null
adb shell am dumpheap $(adb shell pgrep terror) /data/local/tmp/heapdump
adb pull /data/local/tmp/heapdump ./heapdump 
strings ./heapdump > heapdumpstrings
