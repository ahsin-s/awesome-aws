import sys
import logging

import torch
import whisper

from shared_constructs.config import LambdaBatchS3SolutionConfig
from shared_constructs.aws.s3 import download_s3, upload_s3


def main():
    logging.info(f"Sys Args: {sys.argv}")
    bucket, key, job_id, user_id = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]

    object_path = LambdaBatchS3SolutionConfig.get_preprocessed_path(user_id, job_id, key)
    print(f"downloading from {object_path}")
    local_object_path = download_s3(bucket, object_path)

    print("loading model")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = whisper.load_model('whisper-small.pt', device=device)
    # Run transcription
    print("running transcription")
    result = model.transcribe(local_object_path)
    text = result['text']
    with open("inference.txt", "w") as f:
        f.write(text)

    print("Uploading transcribed text")
    inference_upload_path = LambdaBatchS3SolutionConfig.get_inference_path(user_id, job_id, key)
    upload_s3("inference.txt", bucket, inference_upload_path)

    return result


if __name__ == "__main__":
    main()
