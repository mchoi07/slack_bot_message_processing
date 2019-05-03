--For importing data to a hive table
use slack;
create external table if not exists messages (
	screen_name string,
	user_id string,
	channel string,
	`time` timestamp,
	text string
)
partitioned by (`date` string, hour string)
stored as orc
location '/user/maria_dev/slackbot_out/';
msck repair table messages;
