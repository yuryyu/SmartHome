# intended to manage the Smart Home system
# insert data to Smart home DB

import paho.mqtt.client as mqtt
# import os
# import time
# import sys, getopt
# import logging
# import queue
import random
from init import *
import data_acq as da


# Define callback functions
def on_log(client, userdata, level, buf):
        print("log: "+buf)
            
def on_connect(client, userdata, flags, rc):    
    if rc==0:
        print("connected OK")                
    else:
        print("Bad connection Returned code=",rc)
        
def on_disconnect(client, userdata, flags, rc=0):    
    print("DisConnected result code "+str(rc))
        
def on_message(client, userdata, msg):
    topic=msg.topic
    m_decode=str(msg.payload.decode("utf-8","ignore"))
    print("message from: " + topic, m_decode)
    insert_DB(topic, m_decode)

def send_msg(client, topic, message):
    print("Sending message: " + message)
    #tnow=time.localtime(time.time())
    client.publish(topic,message)   

def client_init(cname):
    r=random.randrange(1,10000000)
    ID=cname+str(r)
    client = mqtt.Client(ID, clean_session=True) # create new client instance
    # define callback function       
    client.on_connect=on_connect  #bind callback function
    client.on_disconnect=on_disconnect
    client.on_log=on_log
    client.on_message=on_message        
    if username !="":
        client.username_pw_set(username, password)        
    print("Connecting to broker ",broker_ip)
    client.connect(broker_ip,int(port))     #connect to broker
    return client

def insert_DB(topic, m_decode):
    value=parse_data(m_decode)
    if value != 'NA':
        da.add_IOT_data(m_decode.split('From: ')[1].split(' Temperature: ')[0], da.timestamp(), value)
        # TODO - update IOT device last_updated
def parse_data(m_decode):
    value = 'NA'
    # 'From: ' + self.name+ ' Temperature: '+str(temp)+' Humidity: '+str(hum)
    value = m_decode.split(' Temperature: ')[1].split(' Humidity: ')[0]
    return value


def main():    
    cname = "Manager-"
    client = client_init(cname)         
    
    # main monitoring loop
    client.loop_start()  # Start loop
    client.subscribe(comm_topic+'#')
    try:
        while conn_time==0:
            pass
        #time.sleep(conn_time)        
        print("con_time ending") 
    except KeyboardInterrupt:
        client.disconnect() # disconnect from broker
        print("interrrupted by keyboard")

    client.loop_stop()    #Stop loop
    # end session
    client.disconnect() # disconnect from broker
    print("End manager run script")

if __name__ == "__main__":
    main()
