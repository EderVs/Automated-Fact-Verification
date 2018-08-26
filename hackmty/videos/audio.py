from watson_developer_cloud import SpeechToTextV1
from os.path import join, dirname
import json
from pytube import YouTube
import moviepy.editor as mp

speech_to_text = SpeechToTextV1(
    username='d0be84f6-8b82-4541-a8e9-3ff260623f2d',
    password='yoPLWgG0wDPO'
)


def get_text_from_video(url, start_min, start_sec, end_min, end_sec):
    start_time = start_min * 60 + start_sec
    end_time = end_min * 60 + end_sec
    print("Downloading audio...")

    YouTube(url).streams.filter(mime_type="audio/mp4").first().download(filename="audio")

    print("Download succesful")

    mp.AudioFileClip("audio.mp4").write_audiofile("audio.mp3")

    with open("audio.mp3", 'rb') as audio_file:
        speech_recognition_results = speech_to_text.recognize(
            audio = audio_file,
            content_type = "audio/mp3"
        )
    texts = []
    for result in speech_recognition_results.get('results', [{}]):
        texts.append(result.get('alternatives', [{}])[0].get('transcript', ''))
    text = "\n".join(texts)
    print(text)
    return text 
