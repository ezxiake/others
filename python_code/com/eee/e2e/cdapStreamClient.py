'''
Created on Jul 14, 2017

@author: ezxiake
'''

from cdap_stream_client import Config
from cdap_stream_client import StreamClient

config = Config()
config.host = 'localhost'
config.port = 11015
config.namespace = 'production'
config.ssl = False

stream_client = StreamClient(config)
stream_writer = stream_client.create_writer("pubnubIngress")
stream_promise = stream_writer.write("test")
print(stream_promise)
