import os
import sys
import logging
import datetime

import boto3
import ffmpeg
from botocore.client import ClientError

s3_client = boto3.client("s3")


def download_s3(bucket: str, key: str) -> str:
    temp_file_path = os.path.basename(key)
    s3_client.download_file(bucket, key, temp_file_path)
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
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def determine_if_conversion_needed(filename):
    if filename.split(".")[-1] in ["mp3", "wav", "m4a", "mpeg", "mov"]:
        return False
    return True


def extract_audio(video_path, audio_path, codec='mp3'):
    try:
        ffmpeg.input(video_path).output(audio_path, acodec=codec).run()
        print(f"Audio extracted and saved to {audio_path}")
    except ffmpeg.Error as e:
        print(f"An error occurred: {e.stderr.decode()}")


def update_conversion_metadata_table(bucket, key, job_id, user_id):
    dynamodb_client = boto3.resource("dynamodb")
    table = dynamodb_client.Table('preprocessed-file-metadata')
    resp = table.put_item(
        Item={
            'user_id': user_id,
            'job_id': job_id,
            'object_key': key,
            'bucket': bucket,
            'trigger_datetime': datetime.datetime.now().isoformat()
        }
    )
    if resp['ResponseMetadata']['HTTPStatusCode'] == 200:
        print("Job metadata succesfully added")
        return True
    print("Job metadata not updated")
    return False


def main():
    print("SYS ARGS: ")
    print(sys.argv)

    bucket = sys.argv[1]
    key = sys.argv[2]
    job_id = sys.argv[3]
    user_id = sys.argv[4]
    file = download_s3(bucket, key)

    converted_filename = os.path.basename(file)
    if determine_if_conversion_needed(file):
        converted_filename = converted_filename.split(".")[0] + ".mp3"
        extract_audio(file, converted_filename)

    upload_key = f"converted/{user_id}/{job_id}/{converted_filename}"

    if upload_s3(converted_filename, bucket, upload_key):
        if update_conversion_metadata_table(bucket, upload_key, job_id, user_id):
            return
        raise Exception("Error during update of preprocessing conversion metadata table")


if __name__ == "__main__":
    main()
