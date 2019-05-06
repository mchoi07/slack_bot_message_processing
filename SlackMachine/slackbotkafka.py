from kafka import KafkaProducer
import json
import os

class slackkafka:

    BOOTSTRAP_SERVERS=os.environ['BOOTSTRAP_SERVERS']

    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers = BOOTSTRAP_SERVERS, value_serializer=lambda m: json.dumps(m).encode('ascii'))
        
    def sendData(self, topic, data):
        self.producer.send(topic, data)
