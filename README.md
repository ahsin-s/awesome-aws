# awesome-aws

This repository contains a generic solution which uses a combination of api gateway + s3 + lambda + batch + dynamodb for large-scale async workloads.

The key architectural challenges addressed by the solution are:
1. api gateway has a hard limit of 10Mb file size in POST requests. To get around this, I setup a lambda that generates a pre-signed url that is used to grant the client app to upload directly to s3, which can handle terabyte size files.
2. Processing large files for inference is best handled async. I created an API gateway endpoint that takes the user_id and object name in the url args and then a lambda is triggerred whenever this endpoint is called. The lambda parses the user_id and object name and generates a job id and triggers a step function. The step function ARN and job_id are stored in dynamodb. The job_id is returned in the response. 
3. The client-side app can poll to check the status of the job by using the job_id and the job-status endpoint. 
4. The step function runs several batch jobs that are highly optimized for specific processing tasks related to transcription of videos. 
5. The client-side app can get the results path using the get-results endpoint and passing the job id in the url args 
6. The completed job metadata is tracked in dynamodb 

Overall, this solution is low-cost, efficient, scalable, and generic enough to be applicable to hundreds of use cases. <br>
Some examples of use cases:
1. Backend for handling image to pdf / pdf to image conversions as a service 
2. Process a video feed to collect all the faces that appear in the video and then compare the faces with a specified face picture to determine if the person is in the video 
3. RAG pipeline for an AI powered app that provides idea validation as a service
4. Application to analyze images/videos/audio for deep fake detection

## structure
`common_code`: this folder contains the code for the `shared_constructs` package which is installed into docker images, and added as a lambda layer, to allow code reusability. I found publishing a package to pypi to be the easiest way to share code throught different pieces of the solution. <br>

`lambda-batch-s3-solution`: the solution code. `batch` contains the code and other files for aws batch jobs. `lambdas` contains the code for lambda functions used. <br>

## Next Steps
I will probably work on additional solution architectures that serve as a generic solution that can fulfill many use cases.<br>
Perhaps I'll create a generic solution for "real-time" processing tasks.<br>
Or maybe a generic solution for data ingress and egress.

