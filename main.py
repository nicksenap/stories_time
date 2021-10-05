import json
from google.cloud import storage
from google.cloud import speech
import youtube_dl


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


ydl_opts = {
    'format': 'bestaudio/best',
    'no_check_certificate': True,
    'outtmpl': 'audio.mp3',
    'quiet': False,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
}


def main():
    # f = open('text.json', 'r')
    # get_text(f)
    download_video("https://www.youtube.com/watch?v=ffSGKjYrFM4")


def download_video(url):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    upload_blob("s4t-input", "audio.mp3", "audio.mp3")
    transcribe_file()


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )


def transcribe_file():
    # Instantiates a client
    client = speech.SpeechClient()

    # The name of the audio file to transcribe
    gcs_uri = "gs://s4t-input/audio.mp3"

    audio = speech.RecognitionAudio(uri=gcs_uri)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="zh-CN",
    )

    operation = client.long_running_recognize(config=config, audio=audio)
    print("Waiting for operation to complete...")
    response = operation.result(timeout=1000)
    # error = operation.error(timeout=1000)
    print(response.results)


def get_text(f):
    data = json.load(f)
    for i in data['results']:
        print(i['alternatives'][0]['transcript'])


if __name__ == '__main__':
    main()
