########### Dev : Baurin Leza ############
# Cliente MQTT de pruebas


import paho.mqtt.client as mqtt
import sys
import random


class StationDiY():

    def __init__(self, username = "", password = "", device = "", actioner = "", data_actioner = "", sensor = "", data = "", longitud = "", latitud = ""):
        

        self.device = device
        self.sensor = sensor
        self.data = data
        self.actioner = actioner
        self.data_actioner = data_actioner
        self.longitud = longitud
        self.latitud = latitud


    def login(self, username, password):
        """ Save auth credentials to objects return """

        self.username = username
        self.password = password
        

    def sendMQTT(self):
        """ Send message """

        def on_connect(mqttc, userdata, rc):
            mqttc.publish(topic='StationDiy/',  payload='{"username":"%s","password":"%s","device":"%s","sensor":"%s","data":"%s", "actioner":"%s", "data_actioner":"%s", "longitud":"%s", "latitud": "%s","description":"Lorem Ipsium Dev2..."}'%(self.username, self.password, self.device, self.sensor, self.data, self.actioner, self.data_actioner, self.longitud, self.latitud), qos=0)

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

        self.mqttc = mqtt.Client()
        self.mqttc.on_connect = on_connect
        self.mqttc.on_disconnect = on_disconnect
        self.mqttc.on_message = on_message
        self.mqttc.on_publish = on_publish
        self.mqttc.connect(host="stationdiy.eu", port=1883, keepalive=60, bind_address="")
        self.mqttc.loop_forever()

    def setSensor(self, device, sensor, data):
        """ Set sensor by mqtt """

        self.device = device
        self.sensor = sensor
        self.data = data
        self.sendMQTT()



    def getSensor(self,device,sensor):
        """ Get sensor by http method """
        # Get data
    def setActioner(self, device, actioner, data):
        """ Set actioner data by mqtt """
        # Set data
    def getActioner(self, device, actioner):
        """ Get Actioners by http method """
        # Get Actioner
    def setRemoteAlert(self, device, sensor, actioners):
        """ One sensor is able to actioner more than one actioners """
        # set remote alert
    def subscribeSensor(self, device, sensor, callback):
        """ Subscribe to sensor """
        #subscribe to sensor output
