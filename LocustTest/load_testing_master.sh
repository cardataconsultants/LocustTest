date=$(date +'%F_%H:%M:%S')
locust --headless -f locustfile.py --master --users 500 --spawn-rate 10  -H https://map-staging.cardataconsultants.com --html=./Reporting/report-locust-"$date".html
