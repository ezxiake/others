'''
Created on Jul 17, 2017

@author: ezxiake
'''


import datetime, time, threading, yaml, subprocess, sys, requests
import logging.handlers
from cdap_stream_client import Config
from cdap_stream_client import StreamClient

from multiprocessing import Process
from multiprocessing import Pool

    
def executeSend():
    
    if len(sys.argv) != 2: 
        print('Please enter a parameter, and there is only one, for yaml file name')
        exit()
    
    f = open(sys.argv[1])
    yamlMap = yaml.load(f)
    
    config = Config()
    config.host = 'localhost'
    config.port = 11015
    config.namespace = 'production'
    config.ssl = False
    stream_client = StreamClient(config)
    stream_writer = stream_client.create_writer("pubnubIngress")
    
    msgTotalToSendPerDevice = yamlMap.get('settings4MsgSend').get('msgTotalToSendPerDevice')
    intervalInMsToSend = yamlMap.get('settings4MsgSend').get('intervalInMsToSend')
    DeviceIdPre = yamlMap.get('settings4MsgSend').get('DeviceIdPre')
    DeviceIdCount = yamlMap.get('settings4MsgSend').get('DeviceIdCount')
    
    processings = []
    for dic in range(0, DeviceIdCount):
        processings.append({"stream_writer" : stream_writer, "DeviceId" : DeviceIdPre + str(dic), "msgTotalToSendPerDevice" : msgTotalToSendPerDevice, "intervalInMsToSend" : intervalInMsToSend})
    
    startTime = time.time()
    pool = Pool(DeviceIdCount)
    pool.map(msgSender, processings)
    pool.close()
    pool.join()   
    endTime = time.time()
    print("time :" + str(endTime - startTime))
    
def msgSender(parameters):
    
    for msgid in range(0, parameters["msgTotalToSendPerDevice"]):
        
        v_timestamp = str(int(round(time.time() * 1000)))
        msg = '{"id":"assured.pubnub.source_1-14999252927539282","channel":"assured.pubnub.source_1","timestamp":14999252927539282,"payload":"{\\"DeviceID\\":\\"' + str(parameters["DeviceId"]) + '\\",\\"SeqNo\\":' + str(msgid) + ',\\"TimeStamp\\":\\"' + str(v_timestamp) + '\\",\\"LastContact\\":\\"' + str(v_timestamp) + '\\",\\"Position\\":{\\"Lat\\":\\"47.383824586868286\\",\\"Lon\\":\\"-101.97548815049232\\",\\"Accuracy\\":251,\\"Compass\\":301.01,\\"PTimeStamp\\":\\"1493231058\\"},\\"Battery\\":100,\\"Steps\\":100,\\"Calories\\":25}"}'
        sw = parameters["stream_writer"].write(msg)
        print(str(parameters["DeviceId"]) + '    ' + str(msgid) + '    ' + v_timestamp)
        time.sleep(parameters["intervalInMsToSend"] / 1000)


if __name__ == '__main__': 
    executeSend()