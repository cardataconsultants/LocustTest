date=$(date +'%F_%H:%M:%S')
locust --headless -f locustfile.py --master --users 200 --spawn-rate 10  -H https://api-staging.mi-route.com --html=./Reporting/report-locust-"$date".html