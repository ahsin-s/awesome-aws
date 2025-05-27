#!/bin/bash

deploy_lambdas() {
  lambdas=("pre-signed-url-generator")
  for lambda in "${lambdas[@]}"; do
    rm -f code.zip
    rm -f lambda_function.py .
    cp $lambda/lambda_function.py .
    zip code.zip "lambda_function.py"
    aws lambda update-function-code --function-name $lambda --zip-file fileb://code.zip --profile $AWS_DEPLOYMENT_PROFILE
  done
}

deploy_lambdas