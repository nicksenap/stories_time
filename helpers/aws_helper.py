import boto3
import logging
from botocore.exceptions import ClientError
import os
import time
import json

region_name = 'eu-west-1'
sandbox = boto3.session.Session(
    profile_name='Sandbox', region_name=region_name)
bucket_input_name = "transcribe-input-bucket-000001"
bucket_output_name = "transcribe-output-bucket-000001"


def unique_timestamp():
    time.sleep(0.001)
    return str(round(time.time() * 1000))


def delete_file(bucket_name, filename):
    s3 = sandbox.client('s3')
    s3.delete_object(Bucket=bucket_name, Key=filename)


def download_file(bucket_name, filename, local_filename):
    s3 = sandbox.client('s3')
    response = s3.get_object(Bucket=bucket_name, Key=filename)
    content = response['Body']
    jsonContent = json.loads(content.read())[
        'results']['transcripts'][0]['transcript']
    text_file = open(f'{filename}.txt', "w+")
    text_file.write(jsonContent)
    text_file.close()


def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = sandbox.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def transcribe_file_aws(filename, lang='zh-CN', media_format='mp4'):
    transcribe = sandbox.client('transcribe')

    job_name = f"stories_transcribe_{unique_timestamp()}"
    job_uri = f"s3://{bucket_input_name}/{filename}"
    output_key = f'{filename}-transcribe.json'
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        MediaFormat=media_format,
        LanguageCode=lang,
        OutputBucketName=bucket_output_name,
        OutputKey=output_key
    )
    while True:
        status = transcribe.get_transcription_job(
            TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
        print("Not ready yet...")
        time.sleep(5)
    print(status)
    return output_key


def create_bucket(bucket_name, region=region_name):
    """Create an S3 bucket in a specified region

    If a region is not specified, the bucket is created in the S3 default
    region (us-east-1).

    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :return: True if bucket created, else False
    """

    # Create bucket
    try:
        if region is None:
            s3_client = sandbox.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = sandbox.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def check_if_bucket_exist(bucket_name):
    s3 = sandbox.resource('s3')
    return s3.Bucket(bucket_name) in s3.buckets.all()
