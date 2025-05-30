import sys
import logging

import whisper

def download_s3(bucket: str, key: str) -> str:
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
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    logging.info("Object successfully uploaded")
    return True


def save_transcription_result(transcription_result: str):
    raise NotImplementedError


def main():
    logging.info(f"Sys Args: {sys.argv}")
    bucket, key, job_id, user_id = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]



    model = whisper.load_model('whisper-small.pt')
    # Run transcription
    result = model.transcribe("TestRecording.m4a")

    return result


if __name__ == "__main__":
    main()
