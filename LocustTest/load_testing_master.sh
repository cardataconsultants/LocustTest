#!/bin/bash

echo "Usage"
echo "$0 USERS SPAWN_RATE RUN_TIME"
echo "    Ex. $0 500 0.1 10m"

[ -z "$1" ] && USERS=500      || USERS=$1
[ -z "$2" ] && SPAWN_RATE=0.1 || SPAWN_RATE=$2
[ -z "$3" ] && RUN_TIME=10m   || RUN_TIME=$3

date=$(date +'%F_%H:%M:%S')
locust --headless -f locustfile.py --master --users $USERS --spawn-rate $SPAWN_RATE --run-time=$RUN_TIME -H https://map-staging.cardataconsultants.com --html=./Reporting/report-locust-"$date".html
