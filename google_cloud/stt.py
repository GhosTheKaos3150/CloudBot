import io

from os import environ
import base64

from google.cloud import speech_v1
from google.oauth2 import service_account


def get_stt_transcription(file: bytes):
    credentials = service_account.Credentials.from_service_account_file(environ["CLOUD_JSON"])
    
    client = speech_v1.SpeechClient(credentials=credentials)
    audio = speech_v1.RecognitionAudio(content=base64.b64encode(file))
    
    config = speech_v1.RecognitionConfig(
        encoding=speech_v1.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US")
    
    response = client.recognize(config=config, audio=audio)
    
    print(response)
    
    for result in response.results:
        print(f"Transcript: {result.alternatives[0].transcript}")
    