import time
import boto3
import requests

def transcribe_file(job_name, file_uri, transcribe_client):
    transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={"MediaFileUri": file_uri},
        MediaFormat='wav',
        LanguageCode="pt-BR",
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
                    f"\t{job['TranscriptionJob']['Transcript']['TranscriptFileUri']}."
                )
                return job
            break
        else:
            print(f"Waiting for {job_name}. Current status is {job_status}.")
        time.sleep(10)

def translate(transcribed_text):
    boto3.client(service_name='translate', region_name='us-east-2', use_ssl=True)
    text_to_translate = transcribed_text
    result = translate.translate_text(Text=text_to_translate, 
                SourceLanguageCode="pt", TargetLanguageCode="en")
    print('TranslatedText: ' + result.get('TranslatedText'))
    print('SourceLanguageCode: ' + result.get('SourceLanguageCode'))
    print('TargetLanguageCode: ' + result.get('TargetLanguageCode'))

def main():
    transcribe_client = boto3.client("transcribe")
    file_uri = "s3://test-transcribe/answer2.wav"
    job_name = f"Example-job-{time.time_ns()}"
    transcription_job =  transcribe_file(job_name, file_uri, transcribe_client)
    transcript_simple = requests.get(
        transcription_job["Transcript"]["TranscriptFileUri"]
    ).json()
    print(f"Transcript for job {transcript_simple['jobName']}:")
    print(transcript_simple["results"]["transcripts"][0]["transcript"])
    #Prosegue com a tradução


if __name__ == "__main__":
    main()

