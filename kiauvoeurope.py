import requests, json, time, re
from pprint import pprint

base_url="https://prd.eu-ccapi.kia.com:8080/api/v1/"

class kiauvoeurope:
    session = requests.Session()
#    def __init__(self,
#                 access_token=None,
#                 ):


    def get_session(self):
        return self.session.get(base_url+"user/oauth2/authorize?response_type=code&state=test&client_id=fdc85c00-0a2f-4c64-bcb4-2cfb1500730a&redirect_uri="+base_url+"user/oauth2/redirect")

    def set_language(self):
        return self.session.post(base_url+"user/language", json={"lang":"en"})

    def login(self, username, password):
        return self.session.post(base_url+"user/signin", json={"email": username,"password": password}).json()

    def get_token(self, refreshToken):
        return self.session.post(base_url+"user/oauth2/token", data={"grant_type": "authorization_code", "redirect_uri": base_url+"user/oauth2/redirect", "code": refreshToken}, headers={"Content-Type": "application/x-www-form-urlencoded", "Authorization": "Basic ZmRjODVjMDAtMGEyZi00YzY0LWJjYjQtMmNmYjE1MDA3MzBhOnNlY3JldA=="}).json()

    def register(self):
        return self.session.post(base_url+"spa/notifications/register", data={"pushRegId": "199360397125", "pushType": "GCM", "uuid": "1"}, headers={"ccsp-service-id": "fdc85c00-0a2f-4c64-bcb4-2cfb1500730a"}).json()

    def get_vehicles(self, accessToken, deviceId):
        return self.session.get(base_url+"spa/vehicles", headers={"Authorization": accessToken, "ccsp-device-id": deviceId}).json()

    def get_vehicle_profile(self, accessToken, deviceId, vehicleId):
        return self.session.get(base_url+"spa/vehicles/"+vehicleId+"/profile", headers={"Authorization": accessToken, "ccsp-device-id": deviceId}).json()

    def get_vehicle_status(self, accessToken, deviceId, vehicleId):
        return self.session.get(base_url+"spa/vehicles/"+vehicleId+"/status", headers={"Authorization": accessToken, "ccsp-device-id": deviceId}).json()


