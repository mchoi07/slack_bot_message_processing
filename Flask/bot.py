
#import libaries
import os
#import message

from slackclient import SlackClient

class Bot(object):

    def __init__(self):
        super(Bot, self).__init__()
        self.name = 'pythonboardingbot'
        self.emoji = ":robot_face:"
        self.oauth = {"client_id": os.environ.get("CLIENT_ID"),
                                "client_secret": os.environ.get("CLIENT_SECRET"),
                                "scope": "bot"}
        self.verification = os.environ.get("VERIFICATION_TOKEN")

        self.client = SlackClient("")

        self.messages = {}
