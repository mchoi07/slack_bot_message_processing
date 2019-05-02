--For importing data to a hive table
create external table if not exists slackbot (
	screen_name text,
	user_id text,
	channel text,
	time timestamp,
	text text
)
row format delimited
fields terminated by ','
stored as textfile;

load data inpath 'slackbot' into table slackbot;


