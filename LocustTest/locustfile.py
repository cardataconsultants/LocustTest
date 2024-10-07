import csv
import os
from datetime import datetime, timedelta

import dotenv
from locust import HttpUser, task
from locust.exception import StopUser
from filelock import FileLock

import Helper
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

dotenv.load_dotenv()
password = os.environ['password']

def print_now(user_id):
    now = str(datetime.now())
    print("USER ID: "+ user_id + "\n TIMESTAMP: " + now)


def write_user_list():
    test_users_csv = []
    fields = ['username']
    filename = "test_users.csv"
    os.path.dirname(__file__) + "/" + filename
    for prefix in ["FAVR", "CPM", "CAN"]:
        list_of_users = Helper.Helper.get_test_users(170, prefix)
        for i in list_of_users:
            user_check = {"username": i}
            test_users_csv.append(user_check)
    fields = ['username']
    filename = 'test_users.csv'
    lock_path = 'test_users.csv.lock'
    with open(filename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        writer.writerows(test_users_csv)

def get_available_user():
    list_of_users = []
    fields = ['username']
    filename = 'test_users.csv'
    lock_path = 'test_users.csv.lock'
    lock = FileLock(lock_path, timeout=1)
    try:
        with lock.acquire(timeout=1):
            with open(filename) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for row in csv_reader:
                    if row[0] == "username":
                        continue
                    user_check = {"username": row[0]}
                    list_of_users.append(user_check)
            if list_of_users:
                username_check = list_of_users.pop(0)
                username = username_check['username']
                with open(filename, 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=fields)
                    writer.writeheader()
                    writer.writerows(list_of_users)
                return username
            else:
                return None
    except TimeoutError:
        print("Another load testing user currently holds the lock")

write_user_list()
class User(HttpUser):
    user_id = ""
    access_token = ""
    headers = {}
    company_id = ""
    list_of_trips = []
    yesterday = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
    today = (datetime.today()).strftime("%Y-%m-%d")
    cloud_url = os.environ['cloud_api_url']

    @task()
    def maps_get_units(self):
        self.client.get("/api/getUnits/CA")
    @task
    def maps_get_distance(self):
        self.client.get("/api/getDistance?lat1=43.638779&lng1=-79.380653&lat2=43.873810&lng2=-78.963410&country=CA")
    @task()
    def maps_get_geocode(self):
        self.client.get("/api/geocode?street=1600 Pennsylvania Avenue NW&city=Washington&state=DC&zip=20500&country=US")
    @task()
    def maps_get_reverse_geocode(self):
        self.client.get("/api/reverseGeocode?latitude=43.638779&longitude=-79.380653")

    # @task(221)
    # def get_mileage_daily(self):
    #     # print("GETTING MILEAGE FOR: " + str(self.user_id))
    #     #print_now(str(self.user_id))
    #     today = datetime.today().strftime("%Y-%m-%d")
    #     self.client.get("/api/mileage/daily?date=" + today, headers=self.headers)
    #
    # @task(40)
    # def create_tracking_trip(self):
    #     #print_now(str(self.user_id))
    #
    #     # print("CREATING TRACKING TRIP FOR: " + str(self.user_id))
    #     trip = Helper.Helper.generate_tracking_trip_with_location(self.user_id, 43.638660, -79.387802)
    #
    #     response_json = (self.client.post("/api/v3/trip", json=trip, headers=self.headers)).json()
    #     self.list_of_trips.append(response_json)
    #
    # @task(25)
    # def get_user(self):
    #     #print_now(str(self.user_id))
    #
    #     self.client.get("/api/v3/user", headers=self.headers)
    #
    # @task(43)
    # def get_my_trips(self):
    #     #print_now(str(self.user_id))
    #
    #     yesterday = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
    #     today = (datetime.today()).strftime("%Y-%m-%d")
    #     self.client.get(
    #         "/api/v3/trips?trip_type=business;personal;unclassified&start_date=" + yesterday + "&end_date=" + today +
    #         "&page=1",
    #         headers=self.headers)
    #
    # @task(21)
    # def get_company_saved_stops(self):
    #     #print_now(str(self.user_id))
    #
    #     self.client.get(
    #         "/api/company/" + str(self.company_id) + "/driver/" + str(
    #             self.user_id) + "/trip_save_stops?date=" + self.today + "&short_list=1",
    #         headers=self.headers, name='/api/company/{id}/{user_id}/trip_save_stops?date=2024-05-27&amp;short_list=1')
    #
    # @task(33)
    # def get_mileage(self):
    #     #print_now(str(self.user_id))
    #
    #     headers = self.headers
    #     self.client.get("/api/mileage/", headers=headers)
    #
    # @task(7)
    # def patch_tracking_trip(self):
    #     #print_now(str(self.user_id))
    #
    #     headers = self.headers
    #     trip = self.list_of_trips[0]
    #     if trip is None:
    #         return
    #     trip_id = str(trip['id'])
    #     for i in range(1, 4):
    #         payload = {
    #             "trip_id": trip_id,
    #             "attribute": "classification",
    #             "update": {
    #                 "type_id": i
    #             }
    #         }
    #         self.client.patch("/tracking/trip", json=payload, headers=headers)
    #
    # @task(25)
    # def update_user_device(self):
    #     #print_now(str(self.user_id))
    #
    #     iphone = {
    #         "platform": "ios",
    #         "version": "15.4.1",
    #         "model": "iPhone13,2",
    #         "manufacturer": "Apple",
    #         "token": "<token>",
    #         "app_version": "3.5.31",
    #         "build_number": "116"
    #     }
    #
    #     android = {
    #         "platform": "android",
    #         "version": "12.1",
    #         "model": "SamsungS20",
    #         "manufacturer": "Samsung",
    #         "token": "<token>",
    #         "app_version": "3.5.31",
    #         "build_number": "117"
    #     }
    #     devices = [android, iphone]
    #     for i in devices:
    #         self.client.post("/api/user/" + str(self.user_id) + "/device/info", json=i, headers=self.headers, name='/api/user/{id}/device/info')
    #
    # @task(2)
    # def create_manual_trip(self):
    #     #print_now(str(self.user_id))
    #
    #     trip = Helper.Helper.generate_manual_trip("CA", "CA", self.user_id,
    #                                        None, None,
    #                                        None, None)
    #
    #     self.client.post("/api/v3/manualTrip", json=trip, headers=self.headers)
    #
    # @task(7)
    # def get_user_schedule(self):
    #     #print_now(str(self.user_id))
    #
    #     self.client.get("/api/user/" + str(self.user_id) + "/schedule", headers=self.headers, name='/api/user/{user_id}/schedule')
    #
    # @task(16)
    # def get_user_schedule_v4(self):
    #     #print_now(str(self.user_id))
    #
    #     self.client.get("/api/v4/user/" + str(self.user_id) + "/schedule", headers=self.headers, name='/api/v4/user/{user_id}/schedule')
    #
    # # @task(3)
    # # def get_tracking_trips(self):
    # #     response = self.client.get("/tracking/trips", headers=self.headers)
    #
    # @task(2)
    # def get_user(self):
    #     #print_now(str(self.user_id))
    #
    #     self.client.get("/api/user", headers=self.headers)
    #
    # @task(1)
    # def delete_tracking_trip(self):
    #     #print_now(str(self.user_id))
    #
    #     trip = self.list_of_trips.pop()
    #     if trip is None:
    #         return
    #     trip_id = str(trip['id'])
    #     self.client.delete("/tracking/trip/" + trip_id, headers=self.headers, name='/tracking/trip/{trip_id}')
    #
    # #
    # @task(1)
    # def get_static_map(self):
    #     #print_now(str(self.user_id))
    #
    #     lat_1 = "33.6400159"
    #     long_1 = "-84.4195797"
    #     lat_2 = "41.9178922"
    #     long_2 = "-71.122965"
    #     self.client.get(
    #         "/api/v3/static_map?origin_lat=" + lat_1 + "&origin_lng=" + long_1 + "&dest_lat=" + lat_2 + "&dest_lng=" +
    #         long_2,
    #         headers=self.headers)
    #
    # @task
    # def get_stops(self):
    #     #print_now(str(self.user_id))
    #
    #     self.client.get("/api/stops", headers=self.headers)

    def on_start(self):
        username = get_available_user()
        if username is not None:
            response = self.client.post("/api/login",
                                        json={"username": username,
                                              "password": password},
                                        headers=Helper.Helper.basic_header('en'))

            response_json = response.json()
            if response.status_code == 504:
                response = self.client.post("/api/login",
                                            json={"username": username,
                                                  "password": password},
                                            headers=Helper.Helper.basic_header('en'))

                response_json = response.json()
            if "title" in response_json and response_json['title'] == "Unable to Log In":
                print("--UNACTIVATED USER: " + username + " --")
                raise StopUser()
            else:
                print("--SIGNING IN WITH: " + username + " --")

                self.user_id = response_json['user_id']
                self.access_token = response_json['token']
                self.headers = Helper.Helper.token_header_with_language(self.access_token, 'en')
                if "FAVR" in username:
                    self.company_id = "41"
                elif "CAN" in username:
                    self.company_id = "364"
                else:
                    self.company_id = "93"
                for i in range(0, 5):
                    trip = Helper.Helper.generate_tracking_trip_with_location(self.user_id, 43.638660, -79.387802)
                    self.client.post("/api/v3/trip", json=trip, headers=self.headers).json()

                response = self.client.get(
                    "/api/v3/trips?trip_type=business;personal;unclassified&start_date=" + self.yesterday + "&end_date=" +
                    self.today + "&page=1",
                    headers=self.headers)
                response_json = response.json()
                self.list_of_trips = response_json['data']
        else:
            print("NO MORE AVAILABLE USERS")
            raise StopUser()
