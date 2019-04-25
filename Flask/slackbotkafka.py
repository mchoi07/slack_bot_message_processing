#import  threading, time

from kafka import KafkaProducer
import json

topic = "slackbot"
key = "key"
value ={"key":"Hello World"}
#value2 = json.dumps(value)
#value3 = json.loads(value2)
#print(type(value3))

#class SlackbotKafkaProducer(threading.Thread):
#    daemon = True
#    
#    def run(self):
#        producer = KafkaProducer(bootstrap_servers = '127.0.0.1:9092')
#        
#        while True:
#            producer.send(topic,{key, value})
#            time.sleep(1)
            

class slackkafka:
    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers = '127.0.0.1:9092',value_serializer=lambda m: json.dumps(m).encode('ascii'))
        
    def sendData(self, topic, data):
        self.producer.send(topic, data)
        
#test = slackkafka()
#test.sendData(topic, value)
