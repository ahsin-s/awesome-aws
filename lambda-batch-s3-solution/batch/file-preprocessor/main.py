import os
import sys
import logging
import datetime

import boto3
import ffmpeg

from shared_constructs.config import LambdaBatchS3SolutionConfig
from shared_constructs.aws.s3 import download_s3, upload_s3


def determine_if_conversion_needed(filename):
    if filename.split(".")[-1] in ["mp3", "wav", "m4a", "mpeg", "mov"]:
        logging.info("No conversion needed")
        return False
    logging.info("File will be converted")
    return True


def extract_audio(video_path, audio_path, codec='mp3'):
    try:
        print("video path: ", video_path)
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

    raw_upload_path = LambdaBatchS3SolutionConfig.get_raw_file_upload_path(user_id, key)
    file = download_s3(bucket, raw_upload_path)

    converted_filename = os.path.basename(file)
    if determine_if_conversion_needed(file):
        converted_filename = converted_filename.split(".")[0] + ".mp3"
        extract_audio(file, converted_filename)

    upload_key = LambdaBatchS3SolutionConfig.get_preprocessed_path(user_id, job_id, converted_filename)

    if upload_s3(converted_filename, bucket, upload_key):
        if update_conversion_metadata_table(bucket, upload_key, job_id, user_id):
            return
        raise Exception("Error during update of preprocessing conversion metadata table")


if __name__ == "__main__":
    main()
