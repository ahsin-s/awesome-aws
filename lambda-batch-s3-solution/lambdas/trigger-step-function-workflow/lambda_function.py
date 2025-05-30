import datetime
import os
import json
import traceback
import uuid

import boto3

from shared_constructs.aws.s3 import check_object_exists

def put_job_metadata(execution_arn, user_id, object_key, bucket, job_id):
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
        return True
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
    job_id = str(uuid.uuid4())
    step_function_input = json.dumps({
        "bucket": bucket,
        "key": object_key,
        "user_id": user_id,
        "job_id": job_id
    })
    print(f"Running step function with input {step_function_input}")
    stepfunction_client = boto3.client("stepfunctions")
    try:
        resp = stepfunction_client.start_execution(
            stateMachineArn = step_function_arn,
            input = step_function_input,
        )
        execution_arn = resp['executionArn']
        print("Step function triggered")
    except Exception as e:
        traceback.format_exc()
        print("Failed to execute step function")
        raise

    # insert the job id and execution_arn into the jobs table in dynamodb
    if not put_job_metadata(execution_arn, user_id, object_key, bucket, job_id):
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Failed to create the inference job'})
        }

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Success', 'job_id': job_id, 'details': 'check job status using the job_id'})
    }
