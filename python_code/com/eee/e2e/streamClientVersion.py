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


class Sender:
    
    def __init__(self):
        
#         self.log = PyLog("send_msg_to_stream").get_log()
#         self.url = 'http://localhost:11015/v3/namespaces/production/streams/pubnubIngress'
        
        if len(sys.argv) != 2: 
            self.log.error('Please enter a parameter, and there is only one, for yaml file name')
            exit()
        
        f = open(sys.argv[1])
        self.yamlMap = yaml.load(f)
        
        config = Config()
        config.host = 'localhost'
        config.port = 11015
        config.namespace = 'production'
        config.ssl = False
        stream_client = StreamClient(config)
        self.stream_writer = stream_client.create_writer("pubnubIngress")
        
#         self.log.info('Ready to send messages ...')
        self.executeSend()
        print("end")
        
    def executeSend(self):
        msgTotalToSendPerDevice = self.yamlMap.get('settings4MsgSend').get('msgTotalToSendPerDevice')
        intervalInMsToSend = self.yamlMap.get('settings4MsgSend').get('intervalInMsToSend')
        DeviceIdPre = self.yamlMap.get('settings4MsgSend').get('DeviceIdPre')
        DeviceIdCount = self.yamlMap.get('settings4MsgSend').get('DeviceIdCount')
        
#         threads = []
        processings = []
        for dic in range(0, DeviceIdCount):
#             threads.append(threading.Thread(target=self.msgSender,args=(DeviceIdPre + str(dic), msgTotalToSendPerDevice, intervalInMsToSend)))
#             processings.append(Process(target=self.msgSender,args=(DeviceIdPre + str(dic), msgTotalToSendPerDevice, intervalInMsToSend)))
            processings.append((DeviceIdPre + str(dic), msgTotalToSendPerDevice, intervalInMsToSend
        
#         for thread in threads:
#         for processing in processings:
#             thread.setDaemon(True)
#             processing.start()
#             processing.close()
#             processing.join()
        
        startTime = time.time()
        pool = Pool(DeviceIdCount)
        pool.map(self.msgSender, processings)
        pool.close()
        pool.join()   
        endTime = time.time()
        print("time :" + str(endTime - startTime))
        
#         thread.join()
#         self.log.info('Messages are sent to stream complete.')
        
    def msgSender(self, deviceId, msgTotalToSendPerDevice, intervalInMsToSend):
        
        for msgid in range(0, msgTotalToSendPerDevice):
            
            v_timestamp = str(int(round(time.time() * 1000)))
#             self.log.debug(str(deviceId) + '    ' + str(msgid) + '    ' + v_timestamp)
#             msg = '{"DeviceID":"' + deviceId + '","SeqNo":' + str(msgid) + ',"TimeStamp":"' + v_timestamp + '","LastContact":"' + v_timestamp + '","Position":{"Lat":"47.383824586868286","Lon":"-101.97548815049232","Accuracy":251,"Compass":301.01,"PTimeStamp":"1493231058"},"Battery":100,"Steps":100,"Calories":25}'
            msg = '{"id":"assured.pubnub.source_1-14999252927539282","channel":"assured.pubnub.source_1","timestamp":14999252927539282,"payload":"{\\"DeviceID\\":\\"' + str(deviceId) + '\\",\\"SeqNo\\":' + str(msgid) + ',\\"TimeStamp\\":\\"' + str(v_timestamp) + '\\",\\"LastContact\\":\\"' + str(v_timestamp) + '\\",\\"Position\\":{\\"Lat\\":\\"47.383824586868286\\",\\"Lon\\":\\"-101.97548815049232\\",\\"Accuracy\\":251,\\"Compass\\":301.01,\\"PTimeStamp\\":\\"1493231058\\"},\\"Battery\\":100,\\"Steps\\":100,\\"Calories\\":25}"}'
#             msg = '{"id":"assured.pubnub.source_1-15000133758476536","channel":"assured.pubnub.source_1","timestamp":15000133758476536,"payload":"{\\"DeviceID\\":\\"e2eTest20170714_01_4\\",\\"SeqNo\\":0,\\"TimeStamp\\":\\"1500013370590\\",\\"LastContact\\":\\"1500013370590\\",\\"Position\\":{\\"Lat\\":\\"47.383824586868286\\",\\"Lon\\":\\"-101.97548815049232\\",\\"Accuracy\\":251,\\"Compass\\":301.01,\\"PTimeStamp\\":\\"1493231058\\"},\\"Battery\\":100,\\"Steps\\":100,\\"Calories\\":25}"}'
            
#             r = requests.post(self.url, data=msg)
            sw = self.stream_writer.write(msg)
#             self.log.info(sw)
            print(str(deviceId) + '    ' + str(msgid) + '    ' + v_timestamp)
            time.sleep(intervalInMsToSend / 1000)

# class PyLog:
# 
#     def __init__(self, logFileName):
#         
#         logPath = '.'
#         level = 'DEBUG'
#         logMaxBytes = '10000000'
#         logBackupCount = '100'
#         fileHandlerLevel = 'DEBUG'
#         screenHandlerLevel = 'DEBUG'
# 
#         log_format = '%(asctime)s [%(levelname)s]  %(message)s'
# 
#         DEBUG = logging.DEBUG
#         INFO = logging.INFO
#         ERROR = logging.ERROR
#         WARNING = logging.WARNING
#         CRITICAL = logging.CRITICAL
# 
#         current_date = datetime.date.today() - datetime.timedelta(days=0)
#         log_name = logPath + "/" + logFileName + "_%s.log" % str(current_date).replace('-', '')
#         formatter = logging.Formatter(log_format)
# 
#         self.log = logging.getLogger(logFileName)
#         self.log.setLevel(locals()[level])
# 
#         file_handler = logging.handlers.RotatingFileHandler(log_name, 'a', int(logMaxBytes), int(logBackupCount), "UTF-8")
#         file_handler.setLevel(locals()[fileHandlerLevel])
#         file_handler.setFormatter(formatter)
# 
#         screen_handler = logging.StreamHandler()
#         screen_handler.setFormatter(formatter)
#         screen_handler.setLevel(locals()[screenHandlerLevel])
# 
#         self.log.addHandler(file_handler)
#         self.log.addHandler(screen_handler)
# 
#     def get_log(self):
#         return self.log


if __name__ == '__main__': Sender()