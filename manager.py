# intended to manage the Smart Home system

import paho.mqtt.client as mqtt
import os
import time
import sys, getopt
import logging
import queue
import random
from init import *
from agent import Mqtt_client


    
    

            
def send_msg(client, topic, message):
    print("Sending message: " + message)
    tnow=time.localtime(time.time())
    client.publish(topic,time.asctime(tnow) + message)   

def client_init(cname):
    r=random.randrange(1,100000)
    ID=cname+str(r)

    client = mqtt.Client(ID, clean_session=True) # create new client instance
    # define callback function
    

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
