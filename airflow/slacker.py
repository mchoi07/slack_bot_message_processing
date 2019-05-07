from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

default_args = {
	'owner': 'airflow',
	'depends_on_past': False,
	'start_date': datetime(2015, 6, 1),
	'email': ['airflow@example.com'],
	'email_on_failure': False,
	'email_on_retry': False,
	'retries': 1,
	'retry_delay': timedelta(minutes=5),
}

dag = DAG('slacker', default_args=default_args, schedule_interval=timedelta(minutes=1))

t1 = BashOperator (
	task_id='hive',
	bash_command='hive -f /home/maria_dev/slackbot/slackbot.sql',
	dag=dag
)

t2 = BashOperator (
	task_id='ok',
	bash_command='echo "ok!"',
	dag=dag
)

t2.set_upstream(t1)	
