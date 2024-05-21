date=$(date +'%F_%H:%M:%S')
locust --headless --users 200 --spawn-rate 1 -H https://api-staging.mi-route.com --html=./Reporting/report-locust-"$date".html
