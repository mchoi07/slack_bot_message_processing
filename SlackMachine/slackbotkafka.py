from kafka import KafkaProducer
import json

class slackkafka:
    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers = '127.0.0.1:9092',value_serializer=lambda m: json.dumps(m).encode('ascii'))
        
    def sendData(self, topic, data):
        self.producer.send(topic, data)
