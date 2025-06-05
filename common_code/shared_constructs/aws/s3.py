import os
import logging

import boto3
from botocore.client import ClientError


def get_s3_client(profile_name=None):
    if profile_name:
        session = boto3.Session(profile_name=profile_name)
        s3_client = session.client('s3')
        return s3_client
    return boto3.client('s3')


def check_object_exists(bucket: str, key: str):
    s3_client = get_s3_client()
    resp = s3_client.list_objects_v2(
        Bucket=bucket,
        Prefix=key,
    )
    if not resp.get('Contents'):
        return False
    return True


def download_s3(bucket: str, key: str) -> str:
    s3_client = get_s3_client()

    logging.info(f"Downloading from {bucket} {key}")
    temp_file_path = os.path.basename(key)
    s3_client.download_file(bucket, key, temp_file_path)
    logging.info(f"Successfully downloaded the object to {temp_file_path}")
    return temp_file_path


def upload_s3(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    try:
        logging.info(f"Uploading file to {object_name}")
        s3_client = get_s3_client()
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    logging.info("Object successfully uploaded")
    return True

def list_objects(bucket_name: str, prefix: str = '') -> list:
    """
    List all object keys in an S3 bucket under a specified prefix using pagination.

    Args:
        bucket_name (str): Name of the S3 bucket.
        prefix (str): Prefix filter for the object keys.

    Returns:
        list: A list of object keys (prefixes) found under the given prefix.
    """
    s3_client = boto3.client('s3')
    paginator = s3_client.get_paginator('list_objects_v2')

    object_keys = []

    page_iterator = paginator.paginate(Bucket=bucket_name, Prefix=prefix)

    for page in page_iterator:
        contents = page.get('Contents', [])
        for obj in contents:
            object_keys.append(obj['Key'])

    return object_keys
