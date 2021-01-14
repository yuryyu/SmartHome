# Class of home IOT devices (emulators) like: DHT, Elec meter, water meter and etc.

import sys
import random
from PyQt5 import  QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from init import *
from agent import Mqtt_client 


# Creating Client name - should be unique 
global clientname, CONNECTED
CONNECTED = False
global ON
ON=False
r=random.randrange(1,10000000)
clientname="IOT_client-Id-"+str(r)


class MC(Mqtt_client):
    def __init__(self):
        super().__init__()

    def on_message(self, client, userdata, msg):
            topic=msg.topic
            m_decode=str(msg.payload.decode("utf-8","ignore"))
            print("message from:"+topic, m_decode)
            mainwin.connectionDock.update_btn_state(m_decode)

     
class ConnectionDock(QDockWidget):
    """Main """
    def __init__(self, mc, topic, name):
        QDockWidget.__init__(self)
        
        self.name = name
        self.topic=topic
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
        formLayot=QFormLayout()
        if 'DHT' in self.name: 
            self.ePublisherTopic=QLineEdit()
            self.ePublisherTopic.setText(self.topic)
            self.Temperature=QLineEdit()
            self.Temperature.setText('')
            self.Humidity=QLineEdit()
            self.Humidity.setText('')
                  
            formLayot.addRow("Turn On/Off",self.eConnectbtn)
            formLayot.addRow("Pub topic",self.ePublisherTopic)
            formLayot.addRow("Temperature",self.Temperature)
            formLayot.addRow("Humidity",self.Humidity)

        elif 'Air' in self.name:
            self.eSubscribeTopic=QLineEdit()
            self.eSubscribeTopic.setText(self.topic)
            self.ePushtbtn=QPushButton("", self)
            self.ePushtbtn.setToolTip("Push me")
            self.ePushtbtn.setStyleSheet("background-color: gray")
               
            formLayot.addRow("Turn On/Off",self.eConnectbtn)
            formLayot.addRow("Sub topic",self.eSubscribeTopic)
            formLayot.addRow("Status",self.ePushtbtn)
        # else:
        #     formLayot=QFormLayout()
        #     formLayot.addRow("Turn On/Off",self.eConnectbtn)
        #     formLayot.addRow("Pub topic",self.ePublisherTopic)
        #     formLayot.addRow("Temperature",self.Temperature)
        #     formLayot.addRow("Humidity",self.Humidity)

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
        if 'Air' in self.name:
            self.mc.subscribe_to(self.topic)

    def push_button_click(self):
        self.mc.publish_to(self.ePublisherTopic.text(), '"value":1')


    def update_btn_state(self,text):
        global ON
        if ON:
            self.ePushtbtn.setStyleSheet("background-color: gray")
            ON = False
        else:
            self.ePushtbtn.setStyleSheet("background-color: red")
            ON = True       
     
class MainWindow(QMainWindow):
    
    def __init__(self, args, parent=None):
        QMainWindow.__init__(self, parent)                
        
        # Parse sys arg values
        self.name = args[1]
        self.units = args[2]
        self.topic = comm_topic+args[3]
        self.update_rate = args[4]

        # Init of Mqtt_client class
        #self.mc=Mqtt_client()
        self.mc=MC()

        if 'DHT' in self.name: 
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
        self.connectionDock = ConnectionDock(self.mc,self.topic, self.name)        
       
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
        argv.append('Airconditioner')
        argv.append('Units')
        argv.append('Room')
        argv.append('6')

    mainwin = MainWindow(argv)
    mainwin.show()
    app.exec_()
