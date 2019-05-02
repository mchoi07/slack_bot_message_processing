# slack_bot_message_processing

This project contains the whole pipeline for recording messages from slack channels to AWS and Hadoop

Abstract: Getting message and discussion from slack chennel and process it to S3 and HDFS in realtime and set the batch job for any query or processing for every 6 hr - data in HDFS to Hive and data in S3 to another S3 or RDS in AWS

SlackMachine: Bot written in python using the slack-machine library. Produces messages from channels it resides in to both a kafka topic and a kinesis stream.

Steps to run the bot:
  1. Create bot for your workspace by adding a Custom bot integration.
  2. Add bot to channels of your choice
  3. Download SlackMachine directory
  4. Create virtual environment with: `virtualenv --python=/path/to/python/version/3.7 venv`
  5. Activate virtual environment with: `source venv/bin/activate`
  6. Change directory to SlackMachine: `cd /path/to/SlackMachine`
  7. Install dependencies: `pip install -r requirements.txt`
  8. Set environment variable for slack api token for the bot created above, which can be found in the manage custom configurations menu: `export SLACK_APIT_TOKEN=<your token here>`
  9. Set environment variable for kafka bootstrap server: `export BOOTSTRAP_SERVERS=<your broker address here>`
  10. Run the bot: `slack-machine`
  
Spark Consumer: Spark streaming consumer written in Scala. Gets records from the kafka stream and parses them down to a dataframe consisting of screen_name, user_id, channel, time, and text. Data is then written to hdfs in parquet format in partitions of Date=<YYYYMMdd>/Hour=<HH>.


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
