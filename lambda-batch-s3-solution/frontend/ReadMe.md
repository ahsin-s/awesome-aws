The frontend is a single page app (SPA) that uses <insert JS framework>. 

The frontend accepts user uploads anonymously and performs initial sanitization/validation before performing the logic 
to call the api gateway endpoints to retrieve the pre-signed URL for uploading the file to s3. After that the frontend 
triggers the workflow to process the file while showing a spinning "wait" icon to the user. 

The frontend polls the backend while the spinning icon is showing. Once the backend is done 
processing a pre-signed url to download the file is available and the user clicks a button 
which downloads the transcribed file. 

The frontend does not spin up a webserver, it is deployed on AWS using s3 backend for hosting. This means only HTML, 
CSS, and Javascript are needed for deployment, no need to spin up a webserver. This is a practically free solution for 
hosting and it is very secure. 

Deployment Details
I followed the guide here https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/getting-started-cloudfront-overview.html#getting-started-cloudformation-create-s3-www-bucket 

1. to deploy the domain "example.com" 2 buckets are needed: www.example.com AND example.com. \
The bucket name must be the same as the domain name, and in this case if a user visits www.example.com, they will be
routed to the bucket "www.example.com", and if they visit example.com, they will be routed to the corresponding bucket.
2. Public access to the bucket is blocked. To enable hosting, cloudfront distributes the html/css/js. Cloudfront points 
to s3 as the distribution source, and the bucket policy is setup to only allow the cloudfront principal access to the 
bucket contents. Each bucket needs it's own cloudfront distribution (2 cloudfront distributions in this case). 
3. I created a custom domain using route53
4. I setup the ACM certs following the guide 
5. I setup route53 records with simple routing following the guide
The website is deployed at www.freetranscriptionservice.com

For uploading the website code, I am using deploy.sh bash script which has a simple aws s3 cp command to upload files to
the hosting bucket. 
