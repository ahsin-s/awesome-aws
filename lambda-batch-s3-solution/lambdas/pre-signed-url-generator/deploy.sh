rm -f lambda_code.zip
zip lambda_code.zip lambda_function.py
aws lambda update-function-code --function-name pre-signed-url-generator --zip-file fileb://lambda_code.zip --profile $AWS_DEPLOYMENT_PROFILE
