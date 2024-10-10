#!/bin/bash
# Convenience tool to call master and label the report files with a sys value (either EKS or OLD).

[ -n "$1" ] && sys=$1 || { echo "ERROR: must supply EKS OR old"; exit 1; }
[ -z "$2" ] && USERS=500      || USERS=$1
[ -z "$3" ] && SPAWN_RATE=0.1 || SPAWN_RATE=$2
[ -z "$4" ] && RUN_TIME=10m   || RUN_TIME=$3

cd ~/LocustTest/LocustTest                   && \
./load_testing_master.sh $USERS $SPAWN_RATE $RUN_TIME

cd Reporting                                 && \
rpt=$(ls -lrt | tail -1 | awk '{print $NF}') && \
new=$(echo $rpt | sed 's/html/'$sys'.html/') && \
mv $rpt $new                                 && \
cd ..                                        && \
~/qa-docker/pushReportingToS3.sh             && \
echo                                         && \
echo "Run this on your laptop:"              && \
echo "source ../cd-infra/bucket-cd-infra/set_env.sh staging && aws s3 cp s3://cd-qa/load-testing/$new ~"
echo

