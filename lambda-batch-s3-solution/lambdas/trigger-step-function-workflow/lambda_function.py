import datetime
import os
import json
import uuid

import boto3

def check_object_exists(bucket: str, key: str):
    s3_client = boto3.client("s3")
    resp = s3_client.list_objects_v2(
        Bucket=bucket,
        Prefix=key,
    )
    if not resp.get('Contents'):
        return False
    return True

def put_job_metadata(execution_arn, user_id, object_key, bucket):
    job_id = str(uuid.uuid4())
    dynamodb_client = boto3.resource("dynamodb")
    table = dynamodb_client.Table('batch-jobs-metadata')
    resp = table.put_item(
        Item={
            'user_id': user_id,
            'job_id': job_id,
            'step_function_arn': execution_arn,
            'object_key': object_key,
            'bucket': bucket,
            'trigger_datetime': datetime.datetime.now().isoformat()
        }
    )
    if resp['ResponseMetadata']['HTTPStatusCode'] == 200:
        print("Job metadata succesfully added")
        return job_id
    else:
        print("Job metadata not updated")
    return False

def lambda_handler(event, context):
    user_id = event.get('queryStringParameters', {}).get('user_id')
    object_name = event.get('queryStringParameters', {}).get('object_name')
    object_key = f"uploads/{user_id}/{object_name}"
    bucket = os.environ.get("BUCKET_NAME")
    if not bucket:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "No bucket specified in the lambda"})
        }

    if not check_object_exists(bucket, object_key):
        return {
            "statusCode": 400,
            "body": json.dumps({"message": f"object {object_name} for user {user_id} not found"})
        }

    # setup the step function with environment variables
    # pointing to the object to run inference on
    step_function_arn = os.environ.get("STEP_FUNCTION_ARN")
    step_function_input = json.dumps({
        "bucket": bucket,
        "object_key": object_key
    })

    stepfunction_client = boto3.client("stepfunctions")
    resp = stepfunction_client.start_execution(
        stateMachineArn = step_function_arn,
        input = step_function_input,
    )
    execution_arn = resp['executionArn']

    # insert the job id and execution_arn into the jobs table in dynamodb
    job_id = put_job_metadata(execution_arn, user_id, object_key, bucket)
    if not job_id:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Failed to create the inference job'})
        }

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Success', 'job_id': job_id, 'details': 'check job status using the job_id'})
    }
