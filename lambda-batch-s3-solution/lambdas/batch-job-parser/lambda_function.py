import json

def lambda_handler(event, context):
    # TODO implement
    print("EVENT: ", event)
    print("CONTEXT: ", context)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
