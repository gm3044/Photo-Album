import json
import boto3
import requests
import time
import datetime


def get_custom_labels(bucket, key, etag):
    client = boto3.Session().client('s3')
    try:
        response = client.head_object(
            Bucket=bucket,
            IfMatch=etag,
            Key=key
        )
        return response['Metadata']['customlabels']
    except Exception as e:
        print(e)
        return None



def lambda_handler(event, context):
    
    client = boto3.client('rekognition')
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    etag = event['Records'][0]['s3']['object']['eTag']
    print(bucket, key)
 
    r1 = client.detect_labels(Image= {'S3Object':{'Bucket':bucket,'Name':key}}, MaxLabels=10)
    print(r1)
    
    labels = []
    for label in r1['Labels']:
        labels.append(label['Name'])
    
    print('labels: ', labels)
    
    
    url = "https://search-photos-pakjthtmlypbdrnp4hx33vnyay.us-east-1.es.amazonaws.com/photos/photos"
    headers = {"Content-Type": "application/json"}
    timestamp = time.time()
    openSearch_doc = {
        'objectKey':key,
        'bucket':bucket,
        "createdTimestamp": str(datetime.datetime.now()),
        'x-amz-meta-customLabels' : get_custom_labels(bucket, key, etag),
        'labels':labels
        
    }
    
    r2 = requests.post(url, data=json.dumps(openSearch_doc), auth = ('gm3044','gm3044@E6998'), headers=headers)
    print('hahaha')

    return {
        'statusCode': 200,
        'body': json.dumps('Successfully upload image!')
    }
