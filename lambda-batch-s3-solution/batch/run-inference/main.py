import sys
import logging
import datetime

import boto3
import torch
import whisper

from shared_constructs.config import LambdaBatchS3SolutionConfig
from shared_constructs.aws.s3 import download_s3, upload_s3, list_objects


def get_converted_media(bucket: str, prefix: str) -> str:
    # assuming the specified preprocessed directory (s3 prefix)
    # will have just 1 object and that will be the media
    # that is in a format ready for transcription
    objs = list_objects(bucket, prefix)
    if not objs:
        raise ValueError(f"No objects found under {bucket}/{prefix}")
    key = objs[0]
    downloaded_path = download_s3(bucket, key)
    return downloaded_path


def update_transcribed_text_metadata_table(bucket, key, job_id, user_id):
    dynamodb_client = boto3.resource("dynamodb")
    table = dynamodb_client.Table('transcribed-text-metadata')
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
    logging.info(f"Sys Args: {sys.argv}")
    bucket, key, job_id, user_id = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]

    object_path = LambdaBatchS3SolutionConfig.get_preprocessed_path(user_id, job_id, '')
    print(f"downloading from {object_path}")
    local_object_path = get_converted_media(bucket, object_path)

    print("loading model")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Running on devide {device}")
    model = whisper.load_model('whisper-small.pt', device=device)
    # Run transcription
    print("running transcription")
    result = model.transcribe(local_object_path)
    text = result['text']
    with open("inference.txt", "w") as f:
        f.write(text)

    print("Uploading transcribed text")
    inference_upload_path = LambdaBatchS3SolutionConfig.get_inference_path(user_id, job_id, key)
    if upload_s3("inference.txt", bucket, inference_upload_path):
        print("updating metadata")
        update_transcribed_text_metadata_table(bucket, inference_upload_path, job_id, user_id)
    print("Job Completed Successfully")
    return result


if __name__ == "__main__":
    main()
