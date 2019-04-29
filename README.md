# slack_bot_message_processing

This project contains the whole pipeline for recording messages from slack channels to AWS and Hadoop

Flask - Contains code for flask app which installs bot to a channel, listens for messages and then sends data to Kafka and Kinesis

Abstract: Getting message and discussion from slack chennel and process it to S3 and HDFS in realtime and set the batch job for any query or processing for every 6 hr - data in HDFS to Hive and data in S3 to another S3 or RDS in AWS

Update (4/29/19):
This program utilizes a library called `slack-machine` which can be installed and set up using this link:
https://slack-machine.readthedocs.io/en/latest/user/install.html

A quick synopsis can be as follows:
  1. Set up a virtual environment for python.
    a. Make a directory for your bot.
    b. In that directory, use `virtualenv <name of env>`.
    c. To use it, use `source ./bin/activate`.
  2. Install packages with pip.
    `pip install slack-machine kafka-python boto3`
  3. In the folder, create a file called `local-settings.py` where you can store the tokens and plugins for the bot (more on that soon).
  4. Create a folder called `plugins` and go there. Once there, use `touch __init__py` to initialize any code that may be written here.
  
From there, your bot logic can be written in a separate file. Please refer to https://slack-machine.readthedocs.io/en/latest/plugins/basics.html to get started on creating plugins.
