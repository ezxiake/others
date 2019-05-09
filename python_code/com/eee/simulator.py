'''
Created on Jul 11, 2017

@author: ezxiake
'''
import time
import random
import json
#import messaging as ark
import sys
from kafka import KafkaProducer
from functools import reduce


class Sender:
    def __init__(self, producer, topic):
        self.producer = producer
        self.topic = topic
        
    def send(self, msg):
        self.producer.send(self.topic, msg)

if __name__ == "__main__":
    brokers = sys.argv[1]
        
    kafkaProducer = KafkaProducer(bootstrap_servers=brokers)
    sGpsPos = Sender(kafkaProducer, 'streamGps')
    sTrnCam = Sender(kafkaProducer, 'streamCamera')

    #sGpsPos = ark.Sender('streamGps')
    #sTrnCam = ark.Sender('streamCamera')

    with open("gpsPositions.txt","r") as in_file:
        cont = 0
        for line in in_file:
            ##send gpsPosition Message 
#            if cont%2 == 0:
                #print line
            try:
#                z = json.loads(line)
                sGpsPos.send(line)
#                print z
            except:
                print('invalid json mesage: %s' % line)

            cont+=1
            ##send trend camera message
            ip = "192.176.1."+str(random.randint(1, 5))
            x = random.randint(0, 3)
            cam = "CAM"+str(x)
            #provs
            if x==0:
                cam = "MAINFEEDCAM"
            tm = time.strftime("%d/%m/%Y")
            result = [ip + " - demo ["+tm+" +0100]",
                      "\"GET https://networkedevent.ericsson.net/api/v2/useraction/click/camera/"+cam+" HTTP/1.1\"", 
                      " 204 0 \"https://networkedevent.ericsson.net/api/v2/demo/index.html\" ",
                      "\"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:42.0) Gecko/20100101",
                      "Firefox/42.0\",\"0.000288\",\"synth\",\"318\",\"543\",\"-\""]
            print(result)
            message = reduce(lambda x,y: '%s %s'% (x,y), result)
            print(message)
            sTrnCam.send(message)
            time.sleep(1)
