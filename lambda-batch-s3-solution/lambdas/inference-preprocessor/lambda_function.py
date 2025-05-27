"""
This lambda is intended to be invoked as the entrypoint
of the inference step function pipeline.
"""
import json
import boto3

VALID_EXTENSIONS = [
    'mp3',
    'mp4',
    'wav',
    'jpg',
    'png',
    'jpeg',
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
    bucket = event.get('bucket')
    key = event.get('key')

    if not bucket or not key:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'bucket and key are required inputs to trigger this lambda'})
        }

    if not check_object_exists(bucket, key):
        return {
            'statusCode': 400,
            'body': json.dumps({'error': f'object {key} not found'})
        }

    if not check_object_extension_is_valid(key):
        return {
            'statusCode': 400,
            'body': json.dumps({'error': f'the specified object {key} is not valid. Valid object extensions: {VALID_EXTENSIONS}'})
        }


    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'success', 'bucket': bucket, 'key': key, 'is_valid': True})
    }
