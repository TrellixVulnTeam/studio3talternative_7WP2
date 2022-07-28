
import boto3
import botocore

s3 = boto3.client('s3', aws_access_key_id="AKIAXRKV7N44RZEXM5MY", aws_secret_access_key="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")

images=[ 
        "original/1568712469049-file.svg", 
        "original/1569484439694-file.svg", 
        "original/1569484591706-file.svg", 
        "original/1569738105110-file.svg", 
        "original/1569739952057-file.svg", 
        "original/1569740039628-file.svg", 
        "original/1569740071795-file.svg", 
        "original/1569754508641-file.svg", 
        "original/1569759533779-file.svg", 
        "original/1569759875727-file.svg", 
        "original/1569762909242-file.svg", 
        "original/1569763435691-file.svg", 
        "original/1569763511705-file.svg", 
        "original/1569763594650-file.svg", 
        "original/1569763649640-file.svg", 
        "original/1569763959634-file.svg", 
        "original/1569764211933-file.svg", 
        "original/1569764255088-file.svg", 
        "original/1569764337363-file.svg", 
        "original/1569764396455-file.svg", 
        "original/1569764449857-file.svg", 
        "original/1569764514101-file.svg", 
        "thumbnail/1568712469115-thumbnail-file.svg", 
        "thumbnail/1569484439747-thumbnail-file.svg", 
        "thumbnail/1569484591793-thumbnail-file.svg", 
        "thumbnail/1569738105178-thumbnail-file.svg", 
        "thumbnail/1569739952116-thumbnail-file.svg", 
        "thumbnail/1569740039679-thumbnail-file.svg", 
        "thumbnail/1569740071872-thumbnail-file.svg", 
        "thumbnail/1569754508687-thumbnail-file.svg", 
        "thumbnail/1569759533840-thumbnail-file.svg", 
        "thumbnail/1569759875805-thumbnail-file.svg", 
        "thumbnail/1569762909343-thumbnail-file.svg", 
        "thumbnail/1569763435769-thumbnail-file.svg", 
        "thumbnail/1569763511758-thumbnail-file.svg", 
        "thumbnail/1569763594728-thumbnail-file.svg", 
        "thumbnail/1569763649686-thumbnail-file.svg", 
        "thumbnail/1569763959701-thumbnail-file.svg", 
        "thumbnail/1569764211978-thumbnail-file.svg", 
        "thumbnail/1569764255170-thumbnail-file.svg", 
        "thumbnail/1569764337416-thumbnail-file.svg", 
        "thumbnail/1569764396522-thumbnail-file.svg", 
        "thumbnail/1569764449922-thumbnail-file.svg", 
        "thumbnail/1569764514184-thumbnail-file.svg"
    ]
try:
    for image in images:
        s3.download_file('liveejarinow',image,"images/{}".format(image))
except Exception as e:
    print(e)        
    




