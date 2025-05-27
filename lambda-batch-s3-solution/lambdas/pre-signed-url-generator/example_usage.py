import os
from typing import Tuple, List

import boto3
import requests

def get_presigned_url(user_id: str, filename: str) -> Tuple[str, List]:
    api_gateway_endpoint = os.environ.get("API_GATEWAY_ENDPOINT")
    if not api_gateway_endpoint:
        raise Exception("API_GATEWAY_ENDPOINT environment variable is required")

    presign_response = requests.get(api_gateway_endpoint + f"?user_id={user_id}&object_name={filename}")
    presign_info = presign_response.json()['presignResponse']
    url = presign_info['url']
    fields = presign_info['fields']
    return url, fields

def check_object_successfully_uploaded(user_id: str, filename: str, bucket:str=None):
    session = boto3.Session(profile_name=os.environ.get("AWS_DEPLOYMENT_PROFILE"))
    s3 = session.client("s3")
    if not bucket:
        bucket = os.environ.get("S3_BUCKET")

    prefix = f"uploads/{user_id}"
    resp = s3.list_objects_v2(
        Bucket=bucket,
        Prefix=prefix
    )

    objs = [m['Key'] for m in resp['Contents']]
    if f"{prefix}/{filename}" in objs:
        return True
    return False



def main():
    USER_ID = "user1"
    FILENAME = "lambda_function.py"

    url, fields = get_presigned_url(USER_ID, FILENAME)

    with open(FILENAME, "rb") as f:
        files = {'file': (FILENAME, f)}
        s3_http_response = requests.post(url, data=fields, files=files)  # returns a 204 if successful
    print(s3_http_response)
    print(s3_http_response.text)

    if check_object_successfully_uploaded(USER_ID, FILENAME):
        print("Upload Successful")
    else:
        print("Upload Not Successful!")


if __name__ == "__main__":
    main()