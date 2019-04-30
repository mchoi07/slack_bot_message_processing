import os

SLACK_API_TOKEN= os.environ['SLACK_API_TOKEN']
PLUGINS = [
    'machine.plugins.builtin.general.PingPongPlugin',
    'plugins.listen.EavesdropPlugin'
]
