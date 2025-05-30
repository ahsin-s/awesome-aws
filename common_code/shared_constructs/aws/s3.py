import os
import logging

import boto3
from botocore.client import ClientError


def get_s3_client(profile_name = None):
    if profile_name:
        session = boto3.Session(profile_name=profile_name)
        s3_client = session.client('s3')
        return s3_client
    return boto3.client('s3')


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
