import boto3
import json

def send_video_to_s3(file, file_name):
    # Enviando dado
    bucket1_name = 'trabalho-nabor-ia'
    bucket2_name = 'trabalho-nabor-ia-translate'
    
    s3_client = boto3.client("s3")
    s3_client.put_object(
        Body=file, 
        Bucket=bucket1_name, 
        Key=file_name
    )
    
    s3_client.put_object(
        Body=file, 
        Bucket=bucket2_name, 
        Key=file_name
    )


def get_video_data_from_s3(file_name):
    s3_client = boto3.client("s3")
    
    try:
        bucket1_name = 'trabalho-nabor-ia-out'
        bucket2_name = 'trabalho-nabor-ia-translate-out'
        
        labels = s3_client.get_object(Bucket=bucket1_name, Key=file_name+".json")['Body']
        subtitles = s3_client.get_object(Bucket=bucket2_name, Key=file_name+".srt")['Body']
        
        labels = json.loads(labels.read())
        
        detected_labels = ""
        
        for label in labels:
            detected_labels += f"Detectado: {label['Label']['Name']}, Confiança: {label['Label']['Confidence']}\n"
        
        return detected_labels, subtitles.read()
    
    except Exception as e:
        print(f"Error: {e}")
        
        return 500, 500
    
    