# slack_bot_message_processing

This project contains the whole pipeline for recording messages from slack channels to AWS and Hadoop

Flask - Contains code for flask app which installs bot to a channel, listens for messages and then sends data to Kafka and Kinesis

Abstract: Getting message and discussion from slack chennel and process it to S3 and HDFS in realtime and set the batch job for any query or processing for every 6 hr - data in HDFS to Hive and data in S3 to another S3 or RDS in AWS