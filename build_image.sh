#!/bin/bash

docker build -t sqs_security:latest .
docker tag sqs_security:latest aviv012/sqs_security:latest
docker push aviv012/sqs_security:latest