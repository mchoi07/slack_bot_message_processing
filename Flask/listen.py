from machine.plugins.base import MachineBasePlugin
from machine.plugins.decorators import process
import boto3
from json import JSONEncoder
from kinesis import KinesisProducer
from slackbotkafka import slackkafka
client = boto3.client("kinesis")
kafka_p = slackkafka()
kinesis_p = KinesisProducer(client)



class EavesdropPlugin(MachineBasePlugin):
    
    @process("message")
    def listen2(self, event):
        screen_name = self.users[event['user']]
        event['screen_name']=screen_name.real_name
        print(event)
        if not "subtype" in event:
            kafka_p.sendData("slack", event)
            event_j = JSONEncoder().encode(event)
            kinesis_p.send_to_kinesis(event_j)
