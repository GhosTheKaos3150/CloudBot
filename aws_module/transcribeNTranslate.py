import time
import boto3
import requests
import urllib

# CODIGO DE EXEMPLO PARA PEGAR O TRANSCRITO DE UM S3 #
# https://github.com/awsdocs/aws-doc-sdk-examples/blob/main/python/example_code/transcribe/transcribe_basics.py#L336

def transcribe_file(job_name, file_uri, transcribe_client):
    transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={"MediaFileUri": file_uri},
        MediaFormat='mp4',
        LanguageCode="pt-BR",
	Subtitles = {
        'Formats': ['srt'],
        'OutputStartIndex': 1
   }
    )

    max_tries = 60
    while max_tries > 0:
        max_tries -= 1
        job = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
        job_status = job["TranscriptionJob"]["TranscriptionJobStatus"]
        if job_status in ["COMPLETED", "FAILED"]:
            print(f"Job {job_name} is {job_status}.")
            if job_status == "COMPLETED":
                print(
                    f"Download the transcript from\n"
                    f"\t{job['TranscriptionJob']['Transcript']['TranscriptFileUri']}.\n\n"
                    f"Download the subtitles from\n"
                    f"\t {job['TranscriptionJob']['Subtitles']['SubtitleFileUris']}"
                )
                return job
            break
        else:
            print(f"Waiting for {job_name}. Current status is {job_status}.")
        time.sleep(10)

def get_translate(transcribed_text):
    translate =boto3.client(service_name='translate', region_name='us-east-2', use_ssl=True)
    #text_to_translate = transcribed_text
    result = translate.translate_text(Text=transcribed_text, 
                SourceLanguageCode="pt", TargetLanguageCode="en")
    print('TranslatedText: ' + result.get('TranslatedText'))
    print('SourceLanguageCode: ' + result.get('SourceLanguageCode'))
    print('TargetLanguageCode: ' + result.get('TargetLanguageCode'))
    return result.get('TranslatedText')

def main():
    transcribe_client = boto3.client("transcribe")
    file_uri = "https://trabalho-nabor-ia.s3.us-east-2.amazonaws.com/video_2023-12-07_13-55-12.mp4"
    job_name = f"Example-job-{time.time_ns()}"
    transcription_job =  transcribe_file(job_name, file_uri, transcribe_client)
    transcript_simple = requests.get(
        transcription_job['TranscriptionJob']["Transcript"]["TranscriptFileUri"]
    ).json()

    for uri in transcription_job['TranscriptionJob']['Subtitles']['SubtitleFileUris']:
        response = urllib.request.urlopen(uri)
        content = response.read().decode('utf-8')
        print(f"\n\nresponse.read: {content}\n\n")
    print(f"Transcript for job {transcript_simple['jobName']}:")
    #transcription_items = transcript_simple['results']['items']

    print(transcript_simple["results"]["transcripts"][0]["transcript"])
    #transcription_to_translate = transcript_simple["results"]["transcripts"][0]["transcript"]
    #translated_text = get_translate(transcription_to_translate)
    translatated_sub = get_translate(content)
    with open(f"sub_{job_name}.srt", 'w') as arq:
        arq.write(translatated_sub)
    #Prosegue com a tradução


if __name__ == "__main__":
    main()

