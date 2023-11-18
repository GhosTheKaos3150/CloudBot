import io

from os import environ
import base64

from google.cloud import speech_v1
from google.oauth2 import service_account


def get_stt_transcription(file: bytes):
    credentials = service_account.Credentials.from_service_account_file(environ["CLOUD_JSON"])
    
    client = speech_v1.SpeechClient(credentials=credentials)
    audio = speech_v1.RecognitionAudio(content=file)
    
    config = speech_v1.RecognitionConfig(
        encoding=speech_v1.RecognitionConfig.AudioEncoding.OGG_OPUS,
        sample_rate_hertz=48000,
        language_code="pt-BR")
    
    request = speech_v1.RecognizeRequest(
        config=config,
        audio=audio,
    )
    
    response = client.recognize(request=request).results[0]
        
    return response.alternatives[0].transcript
    