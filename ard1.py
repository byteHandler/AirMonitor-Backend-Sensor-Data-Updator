#!/usr/bin/python
# coding=utf-8
from __future__ import print_function
import serial, struct, sys, time, json,urllib2,httplib,traceback,urllib
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from datetime import date, datetime
import mysql.connector
import json
import paho.mqtt.client as paho
import os
import socket
import ssl
import firebase
import time
awshost = "a2adq3e0j8pbg4-ats.iot.us-west-2.amazonaws.com";
ff = open("yes.txt",'w')
#myMQTTClient = AWSIoTMQTTClient("aqimonitor")
#myMQTTClient.configureEndpoint(awshost, 8883)
#myMQTTClient.configureCredentials("rootCA.pem", "private.pem.key", "certificate.pem.crt")
#myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
#myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
#myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
#myMQTTClient.configureMQTTOperationTimeout(5)  
#myMQTTClient.connect()
#myMQTTClient.publish("aqi_thing/info", "connected", 0)
key = 'E3OFNINYX3RYT3TW'
baseURL = 'https://api.thingspeak.com/update?api_key=%s' % key
#def on_connect(client , userdata , flags, rc):
#	print("connection result :" + str(rc))
#	client.subscribe("#",1)
#def on_message(client,userdata,msg):
#	print("topic:"+msg.topic)
#	print("payload"+str(msg.payload))
#mqttc = paho.Client()
#mqttc.on_connect = on_connect
#mqttc.on_message = on_message
#awsport = 8883
#clientId = "aws_thing1"
#thingName = "aqi_thing"
#caPath = "rootCA.pem"
#certPath = "certificate.pem.crt"
#keyPath = "private.pem.key"
#mqttc.tls_set(caPath,certfile = certPath , keyfile = keyPath,cert_reqs=ssl.CERT_REQUIRED,tls_version = ssl.PROTOCOL_TLSv1_2, ciphers = None)
#mqttc.connect(awshost,awsport,keepalive=60)
#mqttc.loop_forever()
print(baseURL)
fbase = firebase.FirebaseApplication('https://aqimonitor.firebaseio.com')
DEBUG = 0
CMD_MODE = 2
CMD_QUERY_DATA = 4
CMD_DEVICE_ID = 5
CMD_SLEEP = 6
CMD_FIRMWARE = 7
CMD_WORKING_PERIOD = 8
MODE_ACTIVE = 0
MODE_QUERY = 1

#ser = serial.Serial()
#ser.port = "/dev/ttyUSB0"
#ser.baudrate = 9600

#ser.open()
#ser.flushInput()

byte, data = 0, ""

def dump(d, prefix=''):
    print(prefix + ' '.join(x.encode('hex') for x in d))

def construct_command(cmd, data=[]):
    assert len(data) <= 12
    data += [0,]*(12-len(data))
    checksum = (sum(data)+cmd-2)%256
    ret = "\xaa\xb4" + chr(cmd)
    ret += ''.join(chr(x) for x in data)
    ret += "\xff\xff" + chr(checksum) + "\xab"

    if DEBUG:
        dump(ret, '> ')
    return ret

def process_data(d):
    r = struct.unpack('<HHxxBB', d[2:])
    pm25 = r[0]/10.0
    pm10 = r[1]/10.0
    checksum = sum(ord(v) for v in d[2:8])%256
    return [pm25, pm10]

def process_version(d):
    r = struct.unpack('<BBBHBB', d[3:])
    checksum = sum(ord(v) for v in d[2:8])%256
    print("Y: {}, M: {}, D: {}, ID: {}, CRC={}".format(r[0], r[1], r[2], hex(r[3]), "OK" if (checksum==r[4] and r[5]==0xab) else "NOK"))

def read_response():
    byte = 0
    while byte != "\xaa":
        byte = ser.read(size=1)

    d = ser.read(size=9)

    if DEBUG:
        dump(d, '< ')
    return byte + d

def cmd_set_mode(mode=MODE_QUERY):
    ser.write(construct_command(CMD_MODE, [0x1, mode]))
    read_response()

def cmd_query_data():
    ser.write(construct_command(CMD_QUERY_DATA))
    d = read_response()
    values = []
    if d[1] == "\xc0":
        values = process_data(d)
    return values

def cmd_set_sleep(sleep=1):
    mode = 0 if sleep else 1
    ser.write(construct_command(CMD_SLEEP, [0x1, mode]))
    read_response()

def cmd_set_working_period(period):
    ser.write(construct_command(CMD_WORKING_PERIOD, [0x1, period]))
    read_response()

def cmd_firmware_ver():
    ser.write(construct_command(CMD_FIRMWARE))
    d = read_response()
    process_version(d)

def cmd_set_id(id):
    id_h = (id>>8) % 256
    id_l = id % 256
    ser.write(construct_command(CMD_DEVICE_ID, [0]*10+[id_l, id_h]))
    read_response()
def CustomCallBack(client, userdata, message):
	print("32905820985")
	if message.payload[0] == 't':
		data = bytearray(byte(message.payload))
		arduino.write(data)
	else:
		data = bytearray(byte(message.payload))
		arduino.write(data)
arduino = serial.Serial("/dev/ttyACM0")
arduino.boudrate = 9600
#myMQTTClient.subscribe("aqi_thing/data",1,CustomCallBack)
mydb = mysql.connector.connect( host="3.19.108.240",user="root",passwd="imhacker007",port="3306")
mycursor = mydb.cursor()
mycursor.execute("USE aqi")
while True:
	data = arduino.readline()
	f = open("disp.confg","r")
	curr = f.readline()
	arduino.write(curr.encode())
	x = data.strip().split(",")
	print(x)
	#values = cmd_query_data();
	#if values is not None:
	#	x.append(values[0])
	#	x.append(values[1])
#	params = urllib.urlencode({'field1':x[4],'field2':x[5],'field3':x[1],'field4':x[0],'field5':x[2],'field6':x[3],'key' : key })
	headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = httplib.HTTPConnection("api.thingspeak.com")
	try:
	    now = datetime.now()
            now_str = now.strftime('%Y-%m-%d %H:%M:%S')
	    tempurl =  '&field1=%s&field2=%s&field3=%s&field4=%s&field5=%s&field6=%s' % (x[4],x[5],x[1],x[0],x[2],x[3])
	    #print(baseURL+tempurl)
	    conn = urllib2.urlopen(baseURL +tempurl)
	    mydict = {}
	    mydict['timestamp'] = now_str
	    mydict['PM2.5'] = str(x[4])
	    mydict['PM10'] = str(x[5])
	    mydict['MQ135'] = str(x[1])
	    mydict['MQ02'] = str(x[0])
	    mydict['Temperature'] = str(x[2])
	    mydict['Humidity'] = str(x[3])
	    payload = '{"timestamp":"'+now_str+'", "PM2.5":"'+str(x[4])+'", "PM10" :"'+str(x[5])+'", "MQ135" :"'+x[1]+'", "MQ02":"'+str(x[0])+'", "Temperature" :"'+str(x[2])+'", "Humidity" :"'+str(x[3]+'"}')
	  #  print(payload)
#	    myMQTTClient.publish("aqi_thing/data",json.dumps(mydict),0)
	    fbase.post('https://aqimonitor.firebaseio.com',json.dumps(mydict))
	    strr = "INSERT INTO sensor_values VALUES({},{},{},{},{},{},'{}')".format(float(x[4]),float(x[5]),float(x[1]),float(x[0]),float(x[2]),float(x[3]),now_str)
	   # print(strr)
	    mycursor.execute(strr)
	    mydb.commit()
           # print(payload)
	    conn.close()
        except:

            print(traceback.format_exc())
	print(x)
