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
                                download_file,
                                delete_file)
from helpers.template_helper import render_template, write_to_file_and_open

transcribe_file_name = 'audio.wav-transcribe.json.txt'


def main():
    try:
        os.remove("audio.wav-transcribe.json.txt")
    except:
        pass
    url = sys.argv[1]
    video_url, video_id, video_title = download_video(url)
    create_bucket_if_not_exist(bucket_input_name)
    create_bucket_if_not_exist(bucket_output_name)
    upload_file("audio.wav", bucket_input_name, "audio.wav")
    filename = transcribe_file_aws("audio.wav")
    download_file(bucket_output_name, filename, filename)
    clean_up(filename)
    content = render_template(
        transciption_file=transcribe_file_name, title=video_title)
    write_to_file_and_open(content, "story")


def clean_up(filename):
    try:
        delete_file(bucket_input_name, "audio.wav")
        delete_file(bucket_output_name, filename)
        os.remove("audio.wav")
    except:
        pass


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
