--For importing data to a hive table
USE slack;
CREATE EXTERNAL TABLE if NOT EXISTS messages (
	screen_name string,
	user_id string,
	channel string,
	`time` timestamp,
	text string
)
PARTITIONED BY (`date` string, hour string)
STORED AS ORC
LOCATION '/user/maria_dev/slackbot_out/';
MSCK REPAIR TABLE messages;
