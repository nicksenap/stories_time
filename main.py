import json
import sys
import os
from helpers.youtube_helper import download_video
from helpers.aws_helper import (upload_file,
                                transcribe_file_aws,
                                create_bucket,
                                bucket_input_name,
                                bucket_output_name,
                                check_if_bucket_exist,
                                download_file)


def main():
    url = sys.argv[1]
    download_video(url)
    create_bucket_if_not_exist(bucket_input_name)
    create_bucket_if_not_exist(bucket_output_name)
    upload_file("audio.wav", bucket_input_name, "audio.wav")
    filename = transcribe_file_aws("audio.wav")
    # filename = "audio.wav-transcribe.json"
    download_file(bucket_output_name, filename, filename)
    os.remove(filename)


def create_bucket_if_not_exist(bucket_name):
    if(check_if_bucket_exist(bucket_name)):
        print(f"Bucket {bucket_name} already exist")
    else:
        create_bucket(bucket_name)


def get_text(f):
    data = json.load(f)
    for i in data['results']:
        print(i['alternatives'][0]['transcript'])


if __name__ == '__main__':
    main()
