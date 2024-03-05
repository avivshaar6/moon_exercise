import boto3
import json
import os

def return_sqs(region, log_mode):
    sqs = boto3.client('sqs', region_name=region) 
    response = sqs.list_queues()
    print(f"SQS Queues in {region}:")
    for url in response.get('QueueUrls', []):
        print(url)
        queue_name = url.split('/')[-1]
    
        response = sqs.get_queue_attributes(
            QueueUrl=url,
            AttributeNames=['Policy']
        )
        access_policy = response['Attributes']['Policy']
        data = json.loads(access_policy)
        aws_arn = data['Statement'][0]['Principal']['AWS']
        aws_arn_type = type(aws_arn)
        account_id = boto3.client('sts').get_caller_identity().get('Account')

        if aws_arn_type is str:
            if account_id in aws_arn:
                # print(f'Good ARN: {aws_arn}')
                continue
            else:
                with open('log.txt', 'w') as f:
                    f.write(f'{url}.\n')
                print(f'We will update the sqs access policy')
                if log_mode == 'false':    
                  change_root_arn_sqs_policy(sqs, queue_name, region)
        elif aws_arn_type is list:
            for arns in aws_arn:
                if account_id in arns:
                    # print(f'Good ARN: {arns}')
                    continue
                else:
                    with open('log.txt', 'a') as f:
                        f.write(f'{url}.\n')
                    print(f'We will update the sqs access policy')
                    if log_mode == 'false':    
                      change_root_arn_sqs_policy(sqs, queue_name, region)

def get_account_id():
    account_id = boto3.client('sts').get_caller_identity().get('Account')
    return account_id

def change_root_arn_sqs_policy(sqs, queue_name, region):
    account_id = get_account_id()

    change_policy_json = {
        "Version": "2012-10-17",
        "Id": "__default_policy_ID",
        "Statement": [
            {
            "Sid": "__owner_statement",
            "Effect": "Allow",
            "Principal": {
                "AWS": f"arn:aws:iam::{account_id}:root"
            },
            "Action": "SQS:*",
            "Resource": f"arn:aws:sqs:{region}:{account_id}:{queue_name}"
            }
        ]
    }

    response = sqs.set_queue_attributes(
        QueueUrl= f"https://sqs.{region}.amazonaws.com/{account_id}/{queue_name}",
        Attributes={
            'Policy': json.dumps(change_policy_json)
        }
    )

def upload_file(bucket_name):
    s3_client = boto3.client('s3')
    response = s3_client.upload_file('log.txt', bucket_name, 'log.txt')

    print(f"Upload log.txt to s3 buchet name: {bucket_name}")
    return response

def get_all_regions():
    ec2_client = boto3.client('ec2', region_name='us-east-1')
    response = ec2_client.describe_regions()
    regions = [region['RegionName'] for region in response['Regions']]
    return regions


def main(): 
    s3_bucket_name = os.environ['S3_BUCKET_NAME']
    log_mode = os.environ['LOG_MODE']
    all_regions = get_all_regions()

    for region in all_regions:
        return_sqs(region, log_mode)
    upload_file(s3_bucket_name)

main()