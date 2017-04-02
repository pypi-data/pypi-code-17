########### Dev : Baurin Leza ############
# Cliente MQTT de pruebas


import paho.mqtt.client as mqtt
import sys
import random

username = ""

def on_connect(mqttc, userdata, rc):
    mqttc.publish(topic='StationDiy/', 
                      payload='{"username":"%s","password":"%s","device":"%s","sensor":"%s","data":"%s", "actioner":"%s", "data_actioner":"%s", "longitud":"%s", "latitud": "%s","description":"Lorem Ipsium Dev2..."}'%(username_, password_, device_, sensor_, data_, actioner_, data_actioner_, longitud_, latitud_), qos=0)

def on_disconnect(mqttc, userdata, rc):
    print('disconnected...rc=' + str(rc))

def on_message(mqttc, userdata, msg):
    print('message received...')
    print "-->%s"%userdata
    print('topic: ' + msg.topic + ', qos: ' + 
          str(msg.qos) + ', message: ' + str(msg.payload))

def on_publish(mqttc, userdata, mid):
    print('message published')
    mqttc.disconnect()

class StationDiY():

    def __init__(self, username = "", password = "", device = "", actioner = "", data_actioner = "", sensor = "", data = "", longitud = "", latitud = ""):
        
        global username_
        global password_ 
        global device_
        global sensor_
        global data_
        global actioner_
        global data_actioner_
        global longitud_
        global latitud_

        username_ = username
        password_ = password
        device_ = device
        sensor_ = sensor
        data_ = data
        actioner_ = actioner
        data_actioner_ = data_actioner
        longitud_ = longitud
        latitud_ = latitud

        self.mqttc = mqtt.Client()
        self.mqttc.on_connect = on_connect
        self.mqttc.on_disconnect = on_disconnect
        self.mqttc.on_message = on_message
        self.mqttc.on_publish = on_publish
        self.mqttc.connect(host="stationdiy.eu", port=1883, keepalive=60, bind_address="")
        self.mqttc.loop_forever()



