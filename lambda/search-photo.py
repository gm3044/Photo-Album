#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import json
import boto3
import requests
from requests_aws4auth import AWS4Auth
import logging


#config
KEY_ID = 'AKIA3YTK55NFSLI4MFWG' #your ID
region = 'us-east-1'
service='es'
# host = 'https://search-photos-pakjthtmlypbdrnp4hx33vnyay.us-east-1.es.amazonaws.com'
url = 'https://search-photos-pakjthtmlypbdrnp4hx33vnyay.us-east-1.es.amazonaws.com/photos/_search'


# logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)


def opensearch(label):
    
    headers = {"Content-Type": "application/json"}
    
    query = {
        "query": {
            "multi_match": {
              "query": label,
              "fields" : ["labels", "x-amz-meta-customLabels"] 
            }
        }
    }

    r = requests.post(url, data=json.dumps(query), auth = ('gm3044','gm3044@E6998'), headers=headers)
    
    response = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": '*'
        },
        "isBase64Encoded": False
    }   
    
    print("response", r.text)
    # Add the search results to the response
    response['body'] = r.text
    hits = json.loads(response['body'])['hits'].get('hits', [])

    #format response body
    results = []
    for each in hits:
        results.append(each['_source'])
    return results


def lambda_handler(event, context):
    # logger.debug('event={}'.format(event))
    # print(event)
    try:
        
        client = boto3.client('lexv2-runtime')
        lex_response = client.recognize_text(
                botId='UXEZTPFADD', 
                botAliasId='TSTALIASID',
                localeId='en_US',
                sessionId='testuser',
                text= event['queryStringParameters']['q'] )

        info = lex_response['interpretations'][0]['intent']['slots']
        print(info)


        response = []
        new_resp = []


        if info['name'] is not None and info['anothername'] is not None:
            keyword_1 = info['name']['value']['originalValue']
            keyword_2 = info['anothername']['value']['originalValue']
            print(keyword_1)
            print(keyword_2)
            
            os_response1 = opensearch(keyword_1)
            response.extend(os_response1)
            os_response2 = opensearch(keyword_2)
            response.extend(os_response2)
        elif info['name'] is not None:
            print("here")
            keyword_1 = info['name']['value']['originalValue']
            print(keyword_1)   
            os_response1 = opensearch(keyword_1)
            response.extend(os_response1) 
            print("right here!!!!")
            
        
        
        for x in response:
           
            if x['objectKey'] not in [j['objectKey'] for j in new_resp]:
                
                print(x)
                print("put in response")
                new_resp.append(x)
              
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,Accept',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,PUT,GET'
            },
            'body': json.dumps(new_resp)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,Accept',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,PUT,GET'
            },
            'body': json.dumps(str(e))
        }

