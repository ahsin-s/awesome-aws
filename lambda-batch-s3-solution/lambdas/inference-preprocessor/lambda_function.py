"""
This lambda is intended to be invoked as the entrypoint
of the inference step function pipeline.
"""
import json
import boto3

from shared_constructs.config import LambdaBatchS3SolutionConfig

VALID_EXTENSIONS = [
    'mp3',
    'mp4',
    'wav',
    'm4a',
]


def check_object_exists(bucket: str, key: str):
    s3_client = boto3.client("s3")
    resp = s3_client.list_objects_v2(
        Bucket=bucket,
        Prefix=key,
    )
    if not resp.get('Contents'):
        return False
    return True


def check_object_extension_is_valid(object_name: str):
    if object_name.split(".")[-1] in VALID_EXTENSIONS:
        return True
    return False


def lambda_handler(event, context):
    user_id = event.get('user_id')
    job_id = event.get('job_id')
    bucket = event.get('bucket')
    key = event.get('key')

    if not bucket or not key:
        raise ValueError("bucket and key are required inputs to trigger this lambda")

    object_path = LambdaBatchS3SolutionConfig.get_raw_file_upload_path(user_id, key)
    if not check_object_exists(bucket, object_path):
        raise FileNotFoundError(f"object {key} not found")

    if not check_object_extension_is_valid(key):
        raise ValueError(f"the specified object {key} is not valid. Valid object extensions: {VALID_EXTENSIONS}")

    return {
        "bucket": bucket,
        "key": key,
        "job_id": job_id,
        "user_id": user_id
    }
