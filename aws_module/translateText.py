import boto3

translate = boto3.client(service_name='translate', region_name='us-east-2', use_ssl=True)
text_to_translate = 'Ola, mundo.'
result = translate.translate_text(Text=text_to_translate, 
            SourceLanguageCode="pt", TargetLanguageCode="en")
print('TranslatedText: ' + result.get('TranslatedText'))
print('SourceLanguageCode: ' + result.get('SourceLanguageCode'))
print('TargetLanguageCode: ' + result.get('TargetLanguageCode'))