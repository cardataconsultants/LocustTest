date=$(date +'%F_%H:%M:%S')
locust --headless -f locustfile.py --master --users 500 --spawn-rate 0.1 --run-time=10m -H https://map-staging.cardataconsultants.com --html=./Reporting/report-locust-"$date".html
