LOCAL RUN:
----------

1.  On your laptop, get the latest repo of LocustTest:Pull latest repo from https://github.com/cardataconsultants/LocustTest/tree/main/LocustTest
      git clone git@github.com:cardataconsultants/LocustTest.git
      cd LocustTest/LocustTest

2.  Run master:
      ./load_testing_master.sh   # Wait for it to be running (how long?)

3.  Run worker:
      ./load_testing_worker.sh   # It will connect to master and should run for 10 minutes.

4.  Resulting file will be in the reporting folder.


AWS RUN:
--------

0. On your laptop, get the latest repo of qa-docker:
      git clone git@github.com:cardataconsultants/qa-docker.git
      git clone git@github.com:cardataconsultants/cd-infra.git

1.  Open a terminal (A):
      cd qa-docker

2.  ./horse.sh master start   # It may already be running. That's OK. Either way, it should also log in.

3.  On this master server:
      cd ~/LocustTest && git checkout . && git pull && cd LocustTest && ./juka-master.sh EKS
        OR
      cd ~/LocustTest && git checkout . && git pull && cd LocustTest && ./juka-master.sh old

4.  Open a terminal (B):
      cd qa-docker

5   ./horse.sh worker start   # It may already be running. That's OK. Either way, it should also log in.

6.  On this worker server:
      cd ~/LocustTest && git checkout . && git pull && cd LocustTest && ./juka-worker.sh

8.  Retrieve the report file:
      On the master, cut the last line of output, and paste it onto your laptop to run.
      Look for the report in your home dir.

9.  When done all testing, please shut down both servers:
      cd qa-docker
      ./horse.sh master stop
      ./horse.sh worker stop

