# Class of home IOT devices (emulators) like: DHT, Elec meter, water meter and etc.
import sys
import random
from PyQt5 import  QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from init import *
from agent import Mqtt_client
from icecream import ic
from datetime import datetime 

def time_format():
    return f'{datetime.now()}  Emulator|> '
ic.configureOutput(prefix=time_format)
ic.configureOutput(includeContext=False) # use True for including script file context file 
# Creating Client name - should be unique 
global clientname
r=random.randrange(1,10000000)
clientname="IOT_clYT-Id-"+str(r)

class MC(Mqtt_client):
    def __init__(self):
        super().__init__()
    def on_message(self, client, userdata, msg):
            topic=msg.topic
            m_decode=str(msg.payload.decode("utf-8","ignore"))
            ic("message from:"+topic, m_decode)
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
            self.Temperature=QLineEdit()
            self.Temperature.setText('')   
            formLayot.addRow("Turn On/Off",self.eConnectbtn)
            formLayot.addRow("Sub topic",self.eSubscribeTopic)
            formLayot.addRow("Status",self.ePushtbtn)
            formLayot.addRow("Temperature",self.Temperature)        
        elif 'Elec' in self.name:
            self.ePublisherTopic=QLineEdit()
            self.ePublisherTopic.setText(self.topic)
            self.Temperature=QLineEdit()
            self.Temperature.setText('')            
            self.Humidity=QLineEdit()
            self.Humidity.setText('')                  
            formLayot.addRow("Turn On/Off",self.eConnectbtn)
            formLayot.addRow("Pub topic",self.ePublisherTopic)
            formLayot.addRow("Electricity",self.Temperature)
            formLayot.addRow("Water",self.Humidity)
        else:
            self.eSubscribeTopic=QLineEdit()
            self.eSubscribeTopic.setText(self.topic)
            self.ePushtbtn=QPushButton("", self)
            self.ePushtbtn.setToolTip("Push me")
            self.ePushtbtn.setStyleSheet("background-color: gray")
            self.Temperature=QLineEdit()
            self.Temperature.setText('')   
            formLayot.addRow("Turn On/Off",self.eConnectbtn)
            formLayot.addRow("Sub topic",self.eSubscribeTopic)
            formLayot.addRow("Status",self.ePushtbtn)
            formLayot.addRow("Temperature",self.Temperature)
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
    def update_btn_state(self,text):
        if 'Set' in text:
            self.ePushtbtn.setStyleSheet("background-color: green")
            self.Temperature.setText(text.split('Set temperature to: ')[1])
        else:
            self.ePushtbtn.setStyleSheet("background-color: gray")            

class MainWindow(QMainWindow):    
    def __init__(self, args, parent=None):
        QMainWindow.__init__(self, parent)        
        # Parse sys arg values
        self.name = args[1]
        self.units = args[2]
        self.topic = comm_topic+args[3]
        self.update_rate = args[4]
        # Init of Mqtt_client class        
        self.mc=MC()
        if 'DHT' in self.name: 
            # Creating timer for update rate support
            self.timer = QtCore.QTimer(self)
            self.timer.timeout.connect(self.create_data)
            self.timer.start(int(self.update_rate)*1000) # in msec        
        elif 'Meter' in self.name: 
            # Creating timer for update rate support
            self.timer = QtCore.QTimer(self)
            self.timer.timeout.connect(self.create_data_EW)
            self.timer.start(int(self.update_rate)*1000) # in msec        
        elif 'Airconditioner' in self.name:          
            # Creating timer for update rate support
            self.timer = QtCore.QTimer(self)
            self.timer.timeout.connect(self.create_data_Air)
            self.timer.start(int(self.update_rate)*1000) # in msec
        elif 'Freezer' in self.name:          
            # Creating timer for update rate support
            self.timer = QtCore.QTimer(self)
            self.timer.timeout.connect(self.create_data_Fr)
            self.timer.start(int(self.update_rate)*1000) # in msec        
        elif 'Boiler' in self.name:          
            # Creating timer for update rate support
            self.timer = QtCore.QTimer(self)
            self.timer.timeout.connect(self.create_data_Bo)
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
        ic('Next update')
        temp=15+random.randrange(1,10)
        hum=74+random.randrange(1,25)
        current_data= 'From: ' + self.name+ ' Temperature: '+str(temp)+' Humidity: '+str(hum)
        self.connectionDock.Temperature.setText(str(temp))
        self.connectionDock.Humidity.setText(str(hum))
        if not self.mc.connected:
            self.connectionDock.on_button_connect_click()
        self.mc.publish_to(self.topic,current_data)

    def create_data_EW(self):
        ic('Electricity-Water data update')
        hour_delta_w = 0.42/24
        hour_delta_el = (670/17)/24
        elec= format(hour_delta_el+random.randrange(-100,100)/300, '.2f') 
        water=format(hour_delta_w +random.randrange(-10,10)/1000, '.3f')
        current_data= 'From: ' + self.name + ' Electricity: '+str(elec)+' Water: '+str(water)
        self.connectionDock.Temperature.setText(str(elec))
        self.connectionDock.Humidity.setText(str(water))
        if not self.mc.connected:
            self.connectionDock.on_button_connect_click()
        self.mc.publish_to(self.topic,current_data)

    def create_data_Air(self):
        ic('Airconditioner data update')        
        if not self.mc.connected:
            self.connectionDock.on_button_connect_click()
        if not self.mc.subscribed:
            self.mc.subscribe_to(self.topic)

    def create_data_Fr(self):
        ic('Freezer data update')        
        if not self.mc.connected:
            self.connectionDock.on_button_connect_click()
        if not self.mc.subscribed:
            self.mc.subscribe_to(self.topic)
        temp=-5+random.randrange(-10,-5)/10        
        current_data=  'Temperature: '+str(temp)
        self.connectionDock.Temperature.setText(str(temp))        
        self.mc.publish_to(self.topic,current_data)

    def create_data_Bo(self):
        ic('Boiler data update')        
        if not self.mc.connected:
            self.connectionDock.on_button_connect_click()
        if not self.mc.subscribed:
            self.mc.subscribe_to(self.topic)
        temp=80+random.randrange(1,20)/2        
        current_data=  'Temperature: '+str(temp)
        self.connectionDock.Temperature.setText(str(temp))       
        self.mc.publish_to(self.topic,current_data)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    argv=sys.argv
    if len(sys.argv)==1:
        argv.append('airconditioner')
        argv.append('Units')
        argv.append('Room')
        argv.append('6')
    mainwin = MainWindow(argv)
    mainwin.show()
    app.exec_()
