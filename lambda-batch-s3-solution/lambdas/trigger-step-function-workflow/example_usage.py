import os
import requests

api_gateway_endpoint = os.environ.get("API_GATEWAY_ENDPOINT")
endpoint = f"{api_gateway_endpoint}/run-inference?user_id=123&object_name=samplevideo.mp4"

resp = requests.get(endpoint)
print(resp)
print(resp.status_code)
print(resp.text)