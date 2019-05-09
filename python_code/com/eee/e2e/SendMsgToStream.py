'''
Created on Jul 12, 2017

@author: ezxiake
'''


import datetime, time, threading, yaml, subprocess, sys, requests
import logging.handlers
from cdap_stream_client import Config
from cdap_stream_client import StreamClient
# import configparser


class Sender:
    
    def __init__(self):
        
        self.log = PyLog("send_msg_to_stream").get_log()
        self.url = 'http://localhost:11015/v3/namespaces/production/streams/pubnubIngress'
        
        if len(sys.argv) != 2: 
            self.log.error('Please enter a parameter, and there is only one, for yaml file name')
            exit()
        
        f = open(sys.argv[1])
        self.yamlMap = yaml.load(f)
#         print(self.yamlMap)
#         print(self.yamlMap.get('settings4MsgSend').get('DeviceIdPre'))
 
        self.log.info('Ready to send messages ...')
        self.executeSend()
        
    def executeSend(self):
        msgTotalToSendPerDevice = self.yamlMap.get('settings4MsgSend').get('msgTotalToSendPerDevice')
        intervalInMsToSend = self.yamlMap.get('settings4MsgSend').get('intervalInMsToSend')
        DeviceIdPre = self.yamlMap.get('settings4MsgSend').get('DeviceIdPre')
        DeviceIdCount = self.yamlMap.get('settings4MsgSend').get('DeviceIdCount')
        
        threads = []
        for dic in range(0, DeviceIdCount):
            threads.append(threading.Thread(target=self.msgSender,args=(DeviceIdPre + str(dic), msgTotalToSendPerDevice, intervalInMsToSend)))
        
        for thread in threads:
            thread.setDaemon(True)
            thread.start()
        
        thread.join()
        self.log.info('Messages are sent to stream complete.')
        
    def msgSender(self, deviceId, msgTotalToSendPerDevice, intervalInMsToSend):
        
#         subprocess.call('cdap cli', shell=True)
#         subprocess.call('use namespace production', shell=True)
        
        for msgid in range(0, msgTotalToSendPerDevice):
            
            v_timestamp = str(int(round(time.time() * 1000)))
            self.log.debug(str(deviceId) + '    ' + str(msgid) + '    ' + v_timestamp)
#             msg = '{"DeviceID":"' + deviceId + '","SeqNo":' + str(msgid) + ',"TimeStamp":"' + v_timestamp + '","LastContact":"' + v_timestamp + '","Position":{"Lat":"47.383824586868286","Lon":"-101.97548815049232","Accuracy":251,"Compass":301.01,"PTimeStamp":"1493231058"},"Battery":100,"Steps":100,"Calories":25}'
            msg = '{"id":"assured.pubnub.source_1-14999252927539282","channel":"assured.pubnub.source_1","timestamp":14999252927539282,"payload":"{\\"DeviceID\\":\\"' + str(deviceId) + '\\",\\"SeqNo\\":' + str(msgid) + ',\\"TimeStamp\\":\\"' + str(v_timestamp) + '\\",\\"LastContact\\":\\"' + str(v_timestamp) + '\\",\\"Position\\":{\\"Lat\\":\\"47.383824586868286\\",\\"Lon\\":\\"-101.97548815049232\\",\\"Accuracy\\":251,\\"Compass\\":301.01,\\"PTimeStamp\\":\\"1493231058\\"},\\"Battery\\":100,\\"Steps\\":100,\\"Calories\\":25}"}'
#             msg = '{"id":"assured.pubnub.source_1-15000133758476536","channel":"assured.pubnub.source_1","timestamp":15000133758476536,"payload":"{\\"DeviceID\\":\\"e2eTest20170714_01_4\\",\\"SeqNo\\":0,\\"TimeStamp\\":\\"1500013370590\\",\\"LastContact\\":\\"1500013370590\\",\\"Position\\":{\\"Lat\\":\\"47.383824586868286\\",\\"Lon\\":\\"-101.97548815049232\\",\\"Accuracy\\":251,\\"Compass\\":301.01,\\"PTimeStamp\\":\\"1493231058\\"},\\"Battery\\":100,\\"Steps\\":100,\\"Calories\\":25}"}'
            
#             self.log.debug(msg)
            r = requests.post(self.url, data=msg)
#             self.log.info(str(r))
#             self.log.info(r + ' --- ' + msg)
#             stream_promise = self.stream_writer.write(msg)
#             self.log.debug('stream_promise : ' + stream_promise)
#             command_line = 'cdap cli << !' + '\n' + \
#                            'use namespace production' + '\n' + \
#                             'send stream pubnubIngress ' + msg + '\n' + \
#                             'exit' + '\n' + \
#                             '!' 

#             command_line = 'send stream pubnubIngress ' + msg
#             command_line = 'cdap cli << !; use namespace production; send stream pubnubIngress ' + msg + '; exit; !'
                            
#             self.log.debug(command_line)
#             result = subprocess.call(command_line, shell=True)
             
#             if result == 0:
#                 self.log.info('send ' + str(msgid) + ' of ' + deviceId + ' succeed.')
#             else:
#                 self.log.error('send ' + str(msgid) + ' of ' + deviceId + ' failure.')
#             self.log.debug(msg)
#             self.log.debug('\n' + command_line)
            time.sleep(intervalInMsToSend / 1000)

#         subprocess.call('exit', shell=True)
    
class PyLog:

#     def get_cfg(self, section, option):
#     
#         filename = "./e2e.cfg"
#         conf = configparser.ConfigParser()
#         conf.read(filename)
#         return conf.get(section, option)

    def __init__(self, logFileName):

        '''
        log config file eg:
        [logger]
        logPath=.
        level=DEBUG
        logMaxBytes=10000000
        logBackupCount=100
        
        [handler]
        fileHandlerLevel=DEBUG
        screenHandlerLevel=DEBUG
        '''
        
        logPath = '.'
        level = 'DEBUG'
        logMaxBytes = '10000000'
        logBackupCount = '100'
        fileHandlerLevel = 'DEBUG'
        screenHandlerLevel = 'DEBUG'

#         logPath = self.get_cfg("logger", "logPath")
#         level = self.get_cfg("logger", "level")
#         logMaxBytes = self.get_cfg("logger", "logMaxBytes")
#         logBackupCount = self.get_cfg("logger", "logBackupCount")
#         fileHandlerLevel = self.get_cfg("handler", "fileHandlerLevel")
#         screenHandlerLevel = self.get_cfg("handler", "screenHandlerLevel")

        # format = '%(asctime)s [%(levelname)s] [%(filename)s][line:%(lineno)d][%(funcName)s] %(message)s'
        log_format = '%(asctime)s [%(levelname)s]  %(message)s'

        DEBUG = logging.DEBUG
        INFO = logging.INFO
        ERROR = logging.ERROR
        WARNING = logging.WARNING
        CRITICAL = logging.CRITICAL

        current_date = datetime.date.today() - datetime.timedelta(days=0)
        log_name = logPath + "/" + logFileName + "_%s.log" % str(current_date).replace('-', '')
        formatter = logging.Formatter(log_format)

        self.log = logging.getLogger(logFileName)
        self.log.setLevel(locals()[level])

        file_handler = logging.handlers.RotatingFileHandler(log_name, 'a', int(logMaxBytes), int(logBackupCount), "UTF-8")
        file_handler.setLevel(locals()[fileHandlerLevel])
        file_handler.setFormatter(formatter)

        screen_handler = logging.StreamHandler()
        screen_handler.setFormatter(formatter)
        screen_handler.setLevel(locals()[screenHandlerLevel])

        self.log.addHandler(file_handler)
        self.log.addHandler(screen_handler)

    def get_log(self):
        return self.log


if __name__ == '__main__': Sender()

#     log = PyLog("logFileName").get_log()
#     log.debug("debug message")
#     log.info("info message")
#     log.warn("warn message")
#     log.error("error message")
#     log.critical("critical message")

#     Sender()