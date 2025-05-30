#!/bin/bash

rm -rf layer.zip
rm -rf packages
pip install -r requirements.txt --no-cache -t packages
zip -r layer.zip packages/

aws lambda publish-layer-version \
  --layer-name lambda-batch-s3-solution-common \
  --zip-file fileb://layer.zip \
  --compatible-runtimes python3.11 python3.12 python3.13 \
  --description "Common code for lambda" \
  --profile $AWS_DEPLOYMENT_PROFILE


rm -rf layer.zip
rm -rf packages