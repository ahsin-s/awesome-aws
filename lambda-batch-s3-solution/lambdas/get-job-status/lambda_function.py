import json
import boto3

from shared_constructs.config import LambdaBatchS3SolutionConfig


def get_job_arn_from_database(user_id: str, job_id: str):
    """
    Connects to dynamodb and fetches the step function arn
    :param job_id:
    :return:
    """
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(LambdaBatchS3SolutionConfig.JOB_METADATA_TABLE)
    resp = table.get_item(
        Key={
            'user_id': user_id,
            'job_id': job_id,
        }
    )
    if 'Item' in resp.keys():
        item = resp['Item']
        return item.get('step_function_arn')


def lambda_handler(event, context):
    job_id = event.get('queryStringParameters', {}).get('job_id')
    user_id = event.get('queryStringParameters', {}).get('user_id')
    if not job_id or not user_id:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'job_id and user_id are required as a url query parameter'})
        }

    step_function_arn = get_job_arn_from_database(user_id, job_id)
    if not step_function_arn:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': f'job_id {job_id} not found for user {user_id}'})
        }

    stepfunc = boto3.client('stepfunctions')
    describe_resp = stepfunc.describe_execution(executionArn=step_function_arn)
    job_status = describe_resp['status']

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'job status retrieved successfully', 'status': job_status})
    }
