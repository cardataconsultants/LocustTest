date=$(date +'%F_%H:%M:%S')
locust --headless -f locustfile.py --master --users 400 --spawn-rate 2  -H https://api-staging.mi-route.com --html=./Reporting/report-locust-"$date".html
