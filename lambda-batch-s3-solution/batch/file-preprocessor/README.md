all code related to preprocessing the file 

fyi: requirements.txt is being used to manage the python dependencies since using pyproject.toml with poetry would be overkill considering that Docker is being used for deploying the environment


Resources Needed/Deployment Notes:
1. Setting up the batch job was simple - the only trick is that you need to toggle "assign public IP" when creating the job definition
2. The security group attached to the compute resource for the batch job needs to allow ingress/egress for http traffic 
3. The batch job definition must include a task execution role which must have the required permissions (dynamodb and s3 in this case)
4. The dynamodb table used for storing the converted file metadata must be created in advance
5. The step function pipeline must pass container override commands to the aws batch job to allow the output of the upstream lambda to be used as input. The way this is done is to use the "Ref" syntax: 
    ```
    "Submit Batch Job": {
          "Type": "Task",
          "Resource": "arn:aws:states:::batch:submitJob.sync",
          "End": true,
          "Arguments": {
            "JobName": "myBatchJob",
            "JobQueue": "arn:aws:batch:us-east-2:956336999236:job-queue/file-preprocessing-and-inference",
            "JobDefinition": "arn:aws:batch:us-east-2:956336999236:job-definition/file-preprocessor:3",
            "Parameters": "{% $states.input %}",
            "ContainerOverrides": {
              "Command": [
                "Ref::bucket",
                "Ref::key",
                "Ref::job_id",
                "Ref::user_id"
              ]
            }
          }
        }
    ```
