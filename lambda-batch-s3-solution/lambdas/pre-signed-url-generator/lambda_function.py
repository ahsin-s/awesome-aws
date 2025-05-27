import os
import json
import logging

import boto3 
from botocore.exceptions import ClientError


def create_presigned_post(
    bucket_name, object_name, fields=None, conditions=None, expiration=3600
):
    """Generate a presigned URL S3 POST request to upload a file

    :param bucket_name: string
    :param object_name: string
    :param fields: Dictionary of prefilled form fields
    :param conditions: List of conditions to include in the policy
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Dictionary with the following keys:
        url: URL to post to
        fields: Dictionary of form fields and values to submit with the POST
    :return: None if error.
    """

    # Generate a presigned S3 POST URL
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_post(
            bucket_name,
            object_name,
            Fields=fields,
            Conditions=conditions,
            ExpiresIn=expiration,
        )
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL and required fields
    return response

def lambda_handler(event, context):
    user_id = event.get('queryStringParameters', {}).get('user_id')
    object_name = event.get('queryStringParameters', {}).get('object_name')
    if not user_id:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Missing user_id"})
        }
    bucket_name = os.environ['BUCKET_NAME']
    key = f"uploads/{user_id}/{object_name}"

    # Generate pre-signed URL
    try:
        response = create_presigned_post(bucket_name, key)
        return {
            "statusCode": 200,
            "body": json.dumps({"presignResponse": response, "method": "POST"})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": str(e)})
        }
