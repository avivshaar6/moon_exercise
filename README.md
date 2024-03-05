
# Moon_exercise

## AWS SQS Tool

sqs_seurity is a tool written in Python that scans your sqs queues in all regions and deletes unnecessary permission from their access policy, it also uploads a report to the s3 bucket with all the problematic queues.

To run this tool with the docker container please follow these steps:

### Environment Variables
- Configure environment variables:
    - `AWS_ACCESS_KEY_ID = <AWS_ACCESS_KEY_ID>`
    - `AWS_SECRET_ACCESS_KEY = <AWS_SECRET_ACCESS_KEY>`
    - `LOG_MODE = <LOG_MODE>`
    - `S3_BUCKET_NAME = <S3_BUCKET_NAME>`
    - `DOCKERHUB_USERNAME = <DOCKERHUB_USERNAME>`
    - `DOCKERHUB_TOKEN = <DOCKERHUB_TOKEN>`

AWS_ACCESS_KEY_ID - This environment variable is used to provide the access key ID for accessing Amazon Web Services (AWS) resources. AWS uses access keys to authenticate requests made to its services. You should replace <AWS_ACCESS_KEY_ID> with your actual AWS access key ID.

AWS_SECRET_ACCESS_KEY - This environment variable is used to provide the secret access key corresponding to the AWS access key ID mentioned above. The secret access key is used for cryptographic signing of requests to AWS services.

LOG_MODE - This environment variable can be true or false, if you want to run this tool without changing the sqs policy set the `LOG_MODE = true` , to run this tool and change the sqs access policy set `LOG_MODE = false`.

S3_BUCKET_NAME - This environment variable is used to specify the name of the Amazon S3 bucket that this tool will upload the log.txt file.

DOCKERHUB_USERNAME - This environment variable is used to specify the username for Docker Hub.

DOCKERHUB_TOKEN - This environment variable is used in GitHub Actions workflows to authenticate with Docker Hub when pushing Docker images to a repository.

Note: Configure all the environment variables secret in GitHub Actions.



### Workflows

In this repository, we have two workflows:
- ci_sqs_security - This workflow is designed to run on every push to the main branch. It checks out the code, sets up Docker, logs in to Docker Hub using secrets, and builds a Docker image using a custom shell script.
-  ci_sqs_security_daily_docker_job - This workflow is scheduled to run daily at midnight UTC. It checks out the code, sets up Docker, logs in to Docker Hub, and then runs a Docker container with the specified image, passing necessary environment variables for configuration.

## Web App Metadata

This code is a simple web application built using Flask, a web application written in Python. The purpose of this application is to expose instance metadata of an AWS EC2 instance through a REST API endpoint.

This Flask application listens for HTTP requests on port 8080 and exposes a single endpoint /metadata. When a GET request is made to this endpoint, it retrieves the instance metadata of the AWS EC2 instance and returns it as the response.

In this web application, I use IMDSv2 to make the request, to request the top-level metadata items I use the token.


Reference:

- [How IMDSv2 works](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-metadata-v2-how-it-works.html)