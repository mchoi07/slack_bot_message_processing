#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 10:57:02 2019

@author: strato
"""
import boto3

client = boto3.client("kinesis")

class KinesisProducer():
    def __init__(self, client):
        self.client = client
        
    def send_to_kinesis(self, data):
        self.client.put_record(StreamName='slack', Data=data, PartitionKey="Key")
