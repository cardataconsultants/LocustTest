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
      cd qa-docker

1.  Open a terminal (A):

2.  ./horse.sh master start   # It may already be running. That's OK. Either way, it should also log in.

3.  On this master server:
      cd ~/LocustTest && git checkout . && git pull && cd LocustTest && bash load_testing_master.sh 500 0.1 1m; ~/qa-docker/pushReportingToS3.sh && ls -lrt Reporting | tail -1 | awk '{print $NF}'

4.  Open a terminal (B):
      cd qa-docker

5   ./horse.sh worker start   # It may already be running. That's OK. Either way, it should also log in.

6.  On this worker server:
      cd ~/LocustTest && git checkout . && git pull && cd LocustTest && sed -i  's/#--master/--master/g' load_testing_worker.sh && bash load_testing_worker.sh

      ls -lrt Reporting | tail -1 | awk '{print $NF}'  # To get the name of the report you just ran

8.  On your laptop, retrieve the report:
      source ../cd-infra/bucket-cd-infra/set_env.sh staging && cd qa-docker && aws s3 cp s3://cd-qa/load-testing/report-locust-2024-____________.html ~
      Look for the report in your home dir.

NOTE:
For some reason, when I run this on AWS, the reporting is a little wonky and it doesn't produce HTML reports. However, when running on local, it reports correctly. 
