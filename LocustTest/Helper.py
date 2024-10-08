import uuid
from datetime import datetime, timedelta



class Helper:
    token = None
    user_id = None
    tracker_token = None
    refresh_token = None

    @classmethod
    def basic_header(cls, language='en'):
        return {'Accept-Language': language, 'Content-Type': 'application/json'}

    @classmethod
    def token_header(cls, auth_token):
        bearer_token = 'Bearer ' + auth_token
        return {'Authorization': bearer_token}

    @classmethod
    def token_header_with_language(cls, auth_token, language='en'):
        if language is None:
            return cls.token_header(auth_token)
        else:
            bearer_token = 'Bearer ' + auth_token
            return {'Authorization': bearer_token, 'Accept-Language': language, 'Content-Type': 'application/json'}

    @classmethod
    def generate_tracking_trip(cls, user_id, seconds=30, number_of_locations=10, days_in_past=0,
                               latitude=33.89980671314367, longitude=-84.83139826422722,
                               start_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")):
        my_uuid = uuid.uuid4()
        now = (datetime.now() - timedelta(days=days_in_past))
        now = now - timedelta(seconds=(seconds * number_of_locations))
        start_time = start_time
        origin = {"latitude": latitude, "longitude": longitude,
                  "timestamp": start_time}
        new_location = {}
        locations = [origin]
        previous_location = origin
        for i in range(0, number_of_locations):
            now = now + timedelta(seconds=seconds)
            new_location["latitude"] = (previous_location["latitude"] + .0002)
            new_location["longitude"] = (previous_location["longitude"] + .0006)
            new_location["timestamp"] = now.strftime("%Y-%m-%d %H:%M:%S")
            locations.append(new_location.copy())
            previous_location = new_location.copy()
        trip = {}
        trip["destination"] = previous_location.copy()
        trip["origin"] = origin.copy()
        trip["start_time"] = start_time
        trip["end_time"] = previous_location["timestamp"]
        trip["user_id"] = user_id
        trip["locations"] = locations
        trip["trip_date"] = now.strftime("%Y-%m-%d")
        trip["uuid"] = str(my_uuid)
        return trip

    @classmethod
    def generate_manual_trip(cls, country_start, country_end, user_id, driver_origin_namestop=None,
                             driver_destination_namestop=None, company_origin_namestop=None,
                             company_destination_namestop=None, origin_name="Test Start",
                             business_purpose="business trip", trip_date=datetime.now().strftime("%Y-%m-%d")):
        if driver_origin_namestop is not None or driver_destination_namestop is not None:
            assert False, "test code is incomplete. Code needs to be added for none cases"
        if company_origin_namestop is not None or company_destination_namestop is not None:
            assert False, "test code is incomplete. Code needs to be added for none cases"
        trip = {"trip_date": trip_date,
                "sequence_number": -1,
                "user_id": user_id,
                "business_purpose": business_purpose}
        origin = {}
        destination = {}
        if country_start == "CA":
            origin = {
                "driver_stop_id": None,
                "company_stop_id": None,
                "country": "CA",
                "address": "4430 Harvester Rd #2",
                "city": "Burlington",
                "latitude": 43.374833,
                "name": origin_name,
                "state_province": "ON",
                "zip_code": "L7L 4X2",
                "longitude": -79.770425
            }

        elif country_start == "US":
            origin = {
                "driver_stop_id": None,
                "company_stop_id": None,
                "country": "US",
                "address": "434 Massachusetts Avenue",
                "city": "Washington",
                "latitude": 46.184072,
                "name": "Test Start",
                "state_province": "DC",
                "zip_code": "20002",
                "longitude": -73.692927
            }
        if country_end == "CA":
            destination = {
                "driver_stop_id": None,
                "company_stop_id": None,
                "country": "CA",
                "address": "4430 Harvester Rd #2",
                "city": "Burlington",
                "latitude": 43.374833,
                "name": "Test Start",
                "state_province": "ON",
                "zip_code": "L7L 4X2",
                "longitude": -79.770425
            }
        elif country_end == "US":
            destination = {
                "driver_stop_id": None,
                "company_stop_id": None,
                "country": "US",
                "address": "434 Massachusetts Avenue",
                "city": "Washington",
                "latitude": 46.184072,
                "name": "Test Start",
                "state_province": "DC",
                "zip_code": "20002",
                "longitude": -73.692927
            }
        trip["origin"] = origin
        trip["destination"] = destination
        return trip

    @classmethod
    def generate_tracking_trip_with_location(cls, user_id, origin_lat, origin_long, seconds=30, number_of_locations=10, days_in_past=0):
        my_uuid = uuid.uuid4()
        now = (datetime.now() - timedelta(days=days_in_past))
        now = now - timedelta(seconds=(seconds * number_of_locations))
        start_time = now.strftime("%Y-%m-%d %H:%M:%S")
        origin = {"latitude": origin_lat, "longitude": origin_long,
                  "timestamp": now.strftime("%Y-%m-%d %H:%M:%S")}
        new_location = {}
        locations = [origin]
        previous_location = origin
        for i in range(0, number_of_locations):
            now = now + timedelta(seconds=seconds)
            new_location["latitude"] = (previous_location["latitude"] + .0002)
            new_location["longitude"] = (previous_location["longitude"] + .0006)
            new_location["timestamp"] = now.strftime("%Y-%m-%d %H:%M:%S")
            locations.append(new_location.copy())
            previous_location = new_location.copy()
        trip = {}
        trip["destination"] = previous_location.copy()
        trip["origin"] = origin.copy()
        trip["start_time"] = start_time
        trip["end_time"] = previous_location["timestamp"]
        trip["user_id"] = user_id
        trip["locations"] = locations
        trip["trip_date"] = now.strftime("%Y-%m-%d")
        trip["uuid"] = str(my_uuid)
        return trip

    @classmethod
    def get_test_users(cls, user_count, prefix):
        first_name = "Q"
        last_name = "QA"
        array_of_usernames = []
        for i in range(2, user_count + 1):
            username = first_name + last_name + prefix + str(i)
            array_of_usernames.append(username)
        return array_of_usernames
