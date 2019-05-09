'''
Created on Jul 13, 2017

@author: ezxiake
'''
import requests, json
url = 'http://localhost:11015/v3/namespaces/production/streams/pubnubIngress'
# payload = {"DeviceID":"e2eTest20170713_01_3","SeqNo":1,"TimeStamp":"1499914660039","LastContact":"1499914660039","Position":{"Lat":"47.383824586868286","Lon":"-101.97548815049232","Accuracy":251,"Compass":301.01,"PTimeStamp":"1493231058"},"Battery":100,"Steps":100,"Calories":25}
# payload = '{"id":"assured.pubnub.source_1-14999252927539282","channel":"assured.pubnub.source_1","timestamp":14999252927539282,"payload":'{"DeviceID":"e2eTest20170713_01_3","SeqNo":0,"TimeStamp":"1500012498545","LastContact":"1500012498545","Position":{"Lat":"47.383824586868286","Lon":"-101.97548815049232","Accuracy":251,"Compass":301.01,"PTimeStamp":"1493231058"},"Battery":100,"Steps":100,"Calories":25}'}
payload = '{"id":"assured.pubnub.source_1-15000133758476536","channel":"assured.pubnub.source_1","timestamp":15000133758476536,"payload":"{\\"DeviceID\\":\\"e2eTest20170714_01_4\\",\\"SeqNo\\":0,\\"TimeStamp\\":\\"1500013370590\\",\\"LastContact\\":\\"1500013370590\\",\\"Position\\":{\\"Lat\\":\\"47.383824586868286\\",\\"Lon\\":\\"-101.97548815049232\\",\\"Accuracy\\":251,\\"Compass\\":301.01,\\"PTimeStamp\\":\\"1493231058\\"},\\"Battery\\":100,\\"Steps\\":100,\\"Calories\\":25}"}'
# r = requests.post(url, data=json.dumps(payload))
r = requests.post(url, data=payload)
print(r)