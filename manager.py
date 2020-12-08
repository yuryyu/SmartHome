# intended to manage the Smart Home system

import paho.mqtt.client as mqtt
import os
import time
import sys, getopt
import logging
import queue
import random
from init import *


def on_log(client, userdata, level, buf):
    print("log: "+buf)

def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("connected OK")
    else:
        print("Bad connection Returned code=",rc)

def on_disconnect(client, userdata, flags, rc=0):
    print("DisConnected result code "+str(rc))

def on_message(client,userdata,msg):
    topic=msg.topic
    m_decode=str(msg.payload.decode("utf-8","ignore"))
    process_message(client,m_decode,topic)
    print(m_decode)
    
def process_message(client,msg,topic):
    global isengine
    global child
    global belt
    print("message processed: ",topic,msg)
    # decision logic:
    # 1.update engine state:
    if 'engine stopped' in msg:
        isengine = False
        if child and belt:
            send_msg(client, pub_topic, msg_system[3])
    elif 'engine working' in msg:
        isengine = True
    # 2. update child presence in the auto:
    if 'DSP detected' in msg:
        child = True
    elif 'DSP none detected' in msg:
        child = False    
    # 3. update child's belt status:
    if 'belt closed' in msg:
        belt = True 
    elif 'belt opened' in msg:
        belt = False
        send_msg(client, pub_topic, msg_system[2]) 
    # 4. update THD and make decision:
    if 'THD hot' in msg:
        send_msg(client, pub_topic, msg_system[1])
        if child:
            send_msg(client, pub_topic, msg_system[0])

            
def send_msg(client, topic, message):
    print("Sending message: " + message)
    tnow=time.localtime(time.time())
    client.publish(topic,time.asctime(tnow) + message)   

def client_init(cname):
    r=random.randrange(1,100000)
    ID=cname+str(r)

    client = mqtt.Client(ID, clean_session=True) # create new client instance
    # define callback function
    client.on_connect=on_connect  #bind call back function
    client.on_disconnect=on_disconnect
    client.on_log=on_log
    client.on_message=on_message

    if username !="":
        client.username_pw_set(username, password)        
    print("Connecting to broker ",broker_ip)
    client.connect(broker_ip,port)     #connect to broker
    return client

def main():    
    cname = "Manager-"
    client = client_init(cname)

    # main monitoring loop
    client.loop_start()  #Start loop
    for tp in sub_topic:
        client.subscribe(tp)
    try:
        while conn_time==0:
            pass
        time.sleep(conn_time)
        
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
