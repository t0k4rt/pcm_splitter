#!/bin/bash

BASEDIR="$(dirname "$0")"

# trap ctrl-c and call ctrl_c()
trap ctrl_c INT

function ctrl_c() {
        echo "** Trapped CTRL-C"
        echo "Kill all pids"
        kill $LIBRESPOT_PID
        rm $BASEDIR/spotirip
        cat $BASEDIR/tracklist.csv | uniq > $BASEDIR/tracklist_final.csv
        rm $BASEDIR/tracklist.csv 
        /Users/alexandre/.pyenv/shims/python splitter.py $BASEDIR/rip.output.pcm $BASEDIR/tracklist_final.csv false
        exit 0
}

rm $BASEDIR/tracklist_final.csv
mkfifo $BASEDIR/spotirip
$BASEDIR/librespot -n "Spotirip" -b 320 -c $BASEDIR/cache --enable-volume-normalisation --initial-volume 100 --device-type avr --backend pipe --device $BASEDIR/spotirip --onevent $BASEDIR/trackname.sh &
LIBRESPOT_PID=($(ps -ef | grep "librespot" | awk '{ print $2 }'))
echo "launched librespot with pid $LIBRESPOT_PID"

cat $BASEDIR/spotirip > $BASEDIR/rip.output.pcm &
echo "piping output to rip.output.pcm raw pcm file"

# wait for ctrl-c
read -r -d '' _ </dev/tty

