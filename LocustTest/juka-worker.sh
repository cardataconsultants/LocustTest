#!/bin/bash

cd ~/LocustTest/LocustTest                             && \
sed -i 's/#--master/--master/g' load_testing_worker.sh && \
./load_testing_worker.sh
