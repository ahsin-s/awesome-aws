#!/bin/bash

export AWS_DEFAULT_PROFILE=$AWS_DEPLOYMENT_PROFILE
lambdas=(
  "pre-signed-url-generator"
  "trigger-step-function-workflow"
  "inference-preprocessor"
  "get-job-status"
  "batch-job-parser"
)
deploy_lambdas() {
  for lambda in "${lambdas[@]}"; do
    rm -f code.zip
    rm -f lambda_function.py
    cp $lambda/lambda_function.py .
    zip code.zip "lambda_function.py"
    aws lambda update-function-code --function-name $lambda --zip-file fileb://code.zip >> .lambda_deployment_log.txt
  done
  rm -f code.zip
  rm -f lambda_function.py
}

update_lambda_layer_attachment() {
  LATEST_LAYER_VERSION=$(aws lambda list-layer-versions \
  --layer-name lambda-batch-s3-solution-common \
  --query 'LayerVersions[0].Version' \
  --output text)

  DESIRED_LAYER_ARN="arn:aws:lambda:us-east-2:956336999236:layer:lambda-batch-s3-solution-common:$LATEST_LAYER_VERSION"
  echo "DESIRED LAYER ARN: $DESIRED_LAYER_ARN"

  for lambda in "${lambdas[@]}"; do
    CURRENT_LAYERS=$(aws lambda get-function-configuration \
      --function-name "$lambda" \
      --query 'Layers[].Arn' \
      --output text)

    if echo "$CURRENT_LAYERS" | grep -q "$DESIRED_LAYER_ARN"; then
      echo "Layer version already attached to $lambda. No update needed."
    else
      echo "Layer not attached. Updating Lambda configuration..."
      aws lambda update-function-configuration \
        --function-name $lambda \
        --layers "$DESIRED_LAYER_ARN" \
        >> .update_function_layer_log.txt
    fi
  done
}

deploy_lambdas
update_lambda_layer_attachment