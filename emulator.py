# Class of home IOT devices (emulators) like: DHT, Elec meter, water meter and etc.

#import os
import sys
#import PyQt5
import random
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import paho.mqtt.client as mqtt
#import time
#import datetime
from init import *
from agent import Mqtt_client 

#from PyQt5.QtCore import QTimer

# Creating Client name - should be unique 
global clientname, CONNECTED
CONNECTED = False
r=random.randrange(1,10000000)
clientname="IOT_client-Id-"+str(r)

     
class ConnectionDock(QDockWidget):
    """Main """
    def __init__(self, mc, topic):
        QDockWidget.__init__(self)
        
        self.mc = mc
        self.mc.set_on_connected_to_form(self.on_connected)
        self.eHostInput=QLineEdit()
        self.eHostInput.setInputMask('999.999.999.999')
        self.eHostInput.setText(broker_ip)
        
        self.ePort=QLineEdit()
        self.ePort.setValidator(QIntValidator())
        self.ePort.setMaxLength(4)
        self.ePort.setText(broker_port)
        
        self.eClientID=QLineEdit()
        global clientname
        self.eClientID.setText(clientname)
        
        self.eUserName=QLineEdit()
        self.eUserName.setText(username)
        
        self.ePassword=QLineEdit()
        self.ePassword.setEchoMode(QLineEdit.Password)
        self.ePassword.setText(password)
        
        self.eKeepAlive=QLineEdit()
        self.eKeepAlive.setValidator(QIntValidator())
        self.eKeepAlive.setText("60")
        
        self.eSSL=QCheckBox()
        
        self.eCleanSession=QCheckBox()
        self.eCleanSession.setChecked(True)
        
        self.eConnectbtn=QPushButton("Enable/Connect", self)
        self.eConnectbtn.setToolTip("click me to connect")
        self.eConnectbtn.clicked.connect(self.on_button_connect_click)
        self.eConnectbtn.setStyleSheet("background-color: gray")
        
        self.ePublisherTopic=QLineEdit()
        self.ePublisherTopic.setText(topic)

        self.Temperature=QLineEdit()
        self.Temperature.setText('')

        self.Humidity=QLineEdit()
        self.Humidity.setText('')

        formLayot=QFormLayout()       
        formLayot.addRow("Turn On/Off",self.eConnectbtn)
        formLayot.addRow("Pub topic",self.ePublisherTopic)
        formLayot.addRow("Temperature",self.Temperature)
        formLayot.addRow("Humidity",self.Humidity)

        widget = QWidget(self)
        widget.setLayout(formLayot)
        self.setTitleBarWidget(widget)
        self.setWidget(widget)     
        self.setWindowTitle("IOT Emulator") 
        
    def on_connected(self):
        self.eConnectbtn.setStyleSheet("background-color: green")
                    
    def on_button_connect_click(self):
        self.mc.set_broker(self.eHostInput.text())
        self.mc.set_port(int(self.ePort.text()))
        self.mc.set_clientName(self.eClientID.text())
        self.mc.set_username(self.eUserName.text())
        self.mc.set_password(self.ePassword.text())        
        self.mc.connect_to()        
        self.mc.start_listening()

    def push_button_click(self):
        self.mc.publish_to(self.ePublisherTopic.text(), '"value":1')
     
class MainWindow(QMainWindow):
    
    def __init__(self, args, parent=None):
        QMainWindow.__init__(self, parent)                
        
        # Parse sys arg values
        self.name = args[1]
        self.units = args[2]
        self.topic = comm_topic+args[3]
        self.update_rate = args[4]

        # Init of Mqtt_client class
        self.mc=Mqtt_client()
        # Creating timer for update rate support
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.create_data)
        self.timer.start(int(self.update_rate)*1000) # in msec
        
        # general GUI settings
        self.setUnifiedTitleAndToolBarOnMac(True)

        # set up main window
        self.setGeometry(30, 600, 300, 150)
        self.setWindowTitle(self.name)        

        # Init QDockWidget objects        
        self.connectionDock = ConnectionDock(self.mc,self.topic)        
       
        self.addDockWidget(Qt.TopDockWidgetArea, self.connectionDock)        

    def create_data(self):
        print('Next update')
        temp=15+random.randrange(1,10)
        hum=74+random.randrange(1,25)
        current_data= 'From: ' + self.name+ ' Temperature: '+str(temp)+' Humidity: '+str(hum)
        self.connectionDock.Temperature.setText(str(temp))
        self.connectionDock.Humidity.setText(str(hum))
        self.mc.publish_to(self.topic,current_data)
        
if __name__ == '__main__':

    app = QApplication(sys.argv)
    argv=sys.argv
    if len(sys.argv)==1:
        argv.append('TemperaturModule')
        argv.append('Units')
        argv.append('Room')
        argv.append('6')

    mainwin = MainWindow(argv)
    mainwin.show()
    app.exec_()
