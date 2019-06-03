
import requests
import json
# API_ENDPOINT = "http://10.10.0.13:8888/"
def postJson(API_ENDPOINT,command,context):
    data = {'OpCode':command,
            'UUID':context
        }
    try:
        r = requests.post(url = API_ENDPOINT, data=json.dumps(data),timeout=3)
    except requests.exceptions.Timeout:
        pass
