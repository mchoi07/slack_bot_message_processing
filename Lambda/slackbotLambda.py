#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 23:19:03 2019

@author: ichinichi
"""

#imports related to getting data from s3
import json
import boto3
#import related to getting data to RDS
import sys
import slackCredentials
import pymysql
import datetime


#create the client that canconnect to s3
s3_client = boto3.client('s3')
#create the decoder used to deserialize the json
decoder = json.JSONDecoder()

#rds settings
rds_host  = slackCredentials.db_host
name = slackCredentials.db_username
password = slackCredentials.db_password
db_name = slackCredentials.db_name

try:
    conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
except:
    print("ERROR: Unexpected error: Could not connect to MySQL instance.")
    sys.exit()

def lambda_handler(event, context):
    file_obj = event['Records'][0]
    bucketname = file_obj['s3']['bucket']['name']
    filename = file_obj['s3']['object']['key']
    slack_text_object = s3_client.get_object(Bucket=bucketname,Key=filename)
    slack_json_dict = slack_text_object['Body'].read().decode('utf-8')
    
    #I need to parse slack_json_dict because it is multiple jsons without a delimiter
    #going to save file locally then put it into the loop to parse the json
    temp_json_file = open('/tmp/tempjson.txt','w+')
    temp_json_file.write(slack_json_dict)
    temp_json_readable = open('/tmp/tempjson.txt','r')
    temp_json_contents = temp_json_readable.read()
    print(temp_json_contents)
    
    with open('/tmp/tempjson.txt','r') as slack_messy_json_file:
        slack_messy_content = slack_messy_json_file.read()
        content_length = len(slack_messy_content)
        decoder_index = 0
        
        while decoder_index < content_length:
            try:
                obj, decoder_index = decoder.raw_decode(slack_messy_content,decoder_index)
#                print("File index:", decoder_index)
#                print(obj)
#                print(type(obj))
                timestamp = obj['event_ts']
                message = obj['text']
                screen_name = obj['screen_name']
                user_id = obj['user']
                channel = obj['channel']
                datestamp = datetime.datetime.fromtimestamp(float(timestamp))
                cleantime = datestamp.strftime("%Y-%m-%d %H:%M:%S")

#                print('Timestamp is: '+timestamp)
#                print(type(timestamp))
#                print('Messaage is: '+message)
#                print(type(message))
#                print('Screen Name is: '+screen_name)
#                print(type(screen_name))
#                print('User ID is: '+user_id)
#                print(type(user_id))
#                print('The channel is: '+channel)
#                print(type(channel))
            except json.JSONDecodeError as e:
                print("JSONDecodeError:", e)
                decoder_index += 1
                
                
        #section that starts to put information into DS
        try:
            with conn.cursor() as cur:
                cur.execute("DROP TABLE IF EXISTS slackchat")
                cur.execute("CREATE TABLE IF NOT EXISTS slackchat (id INT AUTO_INCREMENT PRIMARY KEY, screen_name VARCHAR(255), message TEXT, user_id VARCHAR(255), channel VARCHAR(255), timestamp TIMESTAMP)")
                sqlQuery = """INSERT INTO slackchat (screen_name, message, user_id, channel, timestamp) VALUES (%s,%s,%s,%s,%s)"""
                sqlData = [(screen_name, message, user_id, channel, cleantime)]
                cur.executemany(sqlQuery,sqlData)
                conn.commit()
        finally:
            conn.close()
       # print(data[0])
    #murr = json.loads(slack_json_dict)
   # print(murr)
    #s3_client.put_object(Body=slack_json_dict,Bucket='slackbotsampleoutput',Key='sample_output.txt')
        
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }


#if __name__ == '__main__':
#    main()
