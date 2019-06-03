import requests
import json


class CallApi:
    device_id = ""
    access_token = ""
    url_endpoint = "https://api.particle.io/v1/devices/"

    def __init__(self,deviceID,accessToken):
        self.device_id=deviceID
        self.access_token=accessToken


    def signalLED(self, deviceid, command):
        access_token = self.access_token
        url_endpoint = self.url_endpoint
        url = url_endpoint + deviceid
        data = {
            'signal': command,
            'access_token': access_token
        }
        r = requests.put(url, data=data)
        print(r)
        print(r.text)

    def claim(self, deviceid):
        access_token = self.access_token
        url_endpoint = self.url_endpoint
        data = {
            'id': deviceid,
            'access_token': access_token
        }
        r = requests.post(url_endpoint, data=data)
        print(r)
        print(r.text)

    def callFunction(self, krwgs):
        access_token = self.access_token
        url_endpoint = self.url_endpoint
        deviceid=self.device_id
        url = url_endpoint + deviceid + "/" + "setURL"
        print(url)
        data = {
            'arg': krwgs,
            'access_token': access_token
        }
        r = requests.post(url, data=data)
        print(r)
        print(r.text)


# if __name__ == "__main__":
#     deviceid = "53004b000951353338363332"
#     # signalLED(device_id,0)
#     api = CallApi()
#     # api.claim(deviceid)
#     # api.signalLED(deviceid,0)
#     rest = json.dumps({"en": "1",
#                        "url": "026269742e6c792f324a3571733779"
#                        })
#     api.callFunction(deviceid, rest)

# 6269742e6c792f324e7073776266
# 776266





'''
    user_name=""
    user_password=""
    device_id="53004b000951353338363332"
    access_token="1cd8d521348bbf62dae33c0c3de436040db3ed52"
    # device_id=""
    url_endpoint="https://api.particle.io/v1/devices/"
    #backUP: "1cd8d521348bbf62dae33c0c3de436040db3ed52"
'''

