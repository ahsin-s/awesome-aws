# Notes 
1. When packaging common code it must be put into a zip file and inside the zip file it needs to go into a folder named "python" otherwise the common code won't be imported. This is very specific for lambda layers. 
2. Permissions for each lambda role were setup manually using the AWS console. A separate role for each lambda is used.
3. each lambda's layer is updated to the latest version of the layer using the deploy_lambda.sh script.
4. 