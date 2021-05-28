import os
import sys
import random
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
BASE_PATH = os.path.abspath(os.path.dirname(__file__))
from init import *
from agent import Mqtt_client 
import time
from icecream import ic
from datetime import datetime 
import data_acq as da

def time_format():
    return f'{datetime.now()}  Emulator|> '

ic.configureOutput(prefix=time_format)
ic.configureOutput(includeContext=False) # use True for including script file context file 

# Creating Client name - should be unique 
global clientname
r=random.randrange(1,10000) # for creating unique client ID
clientname="IOT_clientId-nXLMZeDcjH"+str(r)


class MC(Mqtt_client):
    def __init__(self):
        super().__init__()

    def on_message(self, client, userdata, msg):
            topic=msg.topic            
            m_decode=str(msg.payload.decode("utf-8","ignore"))
            ic("message from:"+topic, m_decode)
            if 'Room_1' in topic:            
                mainwin.airconditionDock.update_temp_win(m_decode.split('Temperature: ')[1].split(' Humidity: ')[0])
            if 'Common' in topic:
                mainwin.airconditionDock.update_temp2_win(m_decode.split('Temperature: ')[1].split(' Humidity: ')[0])
            if 'Home' in topic:
                pass
                #mainwin.airconditionDock.update_temp2_win(m_decode.split('Temperature: ')[1].split(' Humidity: ')[0])

   
class ConnectionDock(QDockWidget):
    """Main """
    def __init__(self,mc):
        QDockWidget.__init__(self)
        
        self.mc = mc
        self.topic = comm_topic+'#'        
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
        
        #self.eUserName=QLineEdit()
        #self.eUserName.setText("MATZI")
        
        #self.ePassword=QLineEdit()
        #self.ePassword.setEchoMode(QLineEdit.Password)
        #self.ePassword.setText("MATZI")
        
        #self.eKeepAlive=QLineEdit()
        #self.eKeepAlive.setValidator(QIntValidator())
        #self.eKeepAlive.setText("60")
        
        #self.eSSL=QCheckBox()
        
        #self.eCleanSession=QCheckBox()
        #self.eCleanSession.setChecked(True)
        
        self.eConnectButton=QPushButton("Connect", self)
        self.eConnectButton.setToolTip("click me to connect")
        self.eConnectButton.clicked.connect(self.on_button_connect_click)
        self.eConnectButton.setStyleSheet("background-color: red")
        
        formLayot=QFormLayout()
        formLayot.addRow("Host",self.eHostInput )
        formLayot.addRow("Port",self.ePort )
        #formLayot.addRow("Client ID", self.eClientID)
        #formLayot.addRow("User Name",self.eUserName )
        #formLayot.addRow("Password",self.ePassword )
        #formLayot.addRow("Keep Alive",self.eKeepAlive )
        #formLayot.addRow("SSL",self.eSSL )
        #formLayot.addRow("Clean Session",self.eCleanSession )
        formLayot.addRow("",self.eConnectButton)

        widget = QWidget(self)
        widget.setLayout(formLayot)
        self.setTitleBarWidget(widget)
        self.setWidget(widget)     
        self.setWindowTitle("Connect") 
        
    def on_connected(self):
        self.eConnectButton.setStyleSheet("background-color: green")
        self.eConnectButton.setObjectName('Connected')
            
    def on_button_connect_click(self):
        self.mc.set_broker(self.eHostInput.text())
        self.mc.set_port(int(self.ePort.text()))
        self.mc.set_clientName(self.eClientID.text())
        #self.mc.set_username(self.eUserName.text())
        #self.mc.set_password(self.ePassword.text())        
        self.mc.connect_to()        
        self.mc.start_listening()
        time.sleep(2)
        if not self.mc.subscribed:
            self.mc.subscribe_to(self.topic)
            
class StatusDock(QDockWidget):
    """Status """

    def __init__(self,mc):
        QDockWidget.__init__(self)
        
        self.mc = mc        

        self.eStatusLivinigAirButton=QPushButton("Status living room aircondition")
        self.eStatusRoomAirButton=QPushButton("Status room aircondition")
        self.eStatusBoilerButton=QPushButton("Status Boiler")
        
        formLayot=QFormLayout()
        formLayot.addRow("", self.eStatusLivinigAirButton)
        formLayot.addRow("",self.eStatusRoomAirButton)
        formLayot.addRow("",self.eStatusBoilerButton)

        widget = QWidget(self)
        widget.setLayout(formLayot)
        self.setTitleBarWidget(widget)
        self.setWidget(widget)     
        self.setWindowTitle("Status") 
        


        #formLayot=QFormLayout()        
        #formLayot.addRow("Topic",self.ePublisherTopic)
        #formLayot.addRow("QOS",self.eQOS)
        #formLayot.addRow("Retain",self.eRetainCheckbox)
        #formLayot.addRow("Message",self.eMessageBox)
        #formLayot.addRow("",self.ePublishButton)
        
        
        #widget = QWidget(self)
        #widget.setLayout(formLayot)
        #self.setWidget(widget) 
        #self.setWindowTitle("Publish")         
       
    def on_button_publish_click(self):
        self.mc.publish_to(self.ePublisherTopic.text(), self.eMessageBox.toPlainText())
        self.ePublishButton.setStyleSheet("background-color: yellow")
        
class GraphsDock(QDockWidget):
    """Graphs """

    def __init__(self,mc):
        QDockWidget.__init__(self)        
        self.mc = mc
        
        self.eElectricityButton = QPushButton("Show",self)

        self.eWaterButton = QPushButton("Show",self)
        self.eWaterButton.clicked.connect(self.on_button_water_click)

        formLayot=QFormLayout()       
        formLayot.addRow("Electricity meter",self.eElectricityButton)
        formLayot.addRow("Water meter",self.eWaterButton)
                
        widget = QWidget(self)
        widget.setLayout(formLayot)
        self.setWidget(widget)
        self.setWindowTitle("Graphs")
        
    def on_button_water_click(self):
       
       da.show_graph_water('WaterMeter')
       self.eWaterButton.setStyleSheet("background-color: yellow")
    
    # create function that update text in received message window
    #def update_mess_win(self,text):
    #    self.eRecMess.append(text)

class TempDock(QDockWidget):
    """Temp """

    def __init__(self,mc):
        QDockWidget.__init__(self)        
        self.mc = mc
    
        self.eBoilerButton = QPushButton("Boiler",self)
        self.eFreezerButton = QPushButton("Freezer",self)
        self.eRefrigeratorButton = QPushButton("Refrigerator",self)
        
        formLayot=QFormLayout()       
        formLayot.addRow("Boiler",self.eBoilerButton)
        formLayot.addRow("Room Freezer",self.eFreezerButton)
        formLayot.addRow("Refrigerator",self.eRefrigeratorButton)

        widget = QWidget(self)
        widget.setLayout(formLayot)
        self.setWidget(widget)
        self.setWindowTitle("Temperature")

class AirconditionDock(QDockWidget):
    """Aircondition """

    def __init__(self,mc):
        QDockWidget.__init__(self)        
        self.mc = mc
    
        self.eLivingButton = QPushButton("Living Room",self)
        self.eLivRoomTemp=QLineEdit()
        self.eLivRoomTemp.setText(" ")

        self.eRoomgButton = QPushButton("Room",self)        
        self.eRoomTemp=QLineEdit()
        self.eRoomTemp.setText(" ")

        formLayot=QFormLayout()       
        formLayot.addRow("Living Room Temperature", self.eLivingButton)
        formLayot.addRow(" ", self.eLivRoomTemp)
        formLayot.addRow("Room Temperature",self.eRoomgButton)
        formLayot.addRow(" ", self.eRoomTemp)

        widget = QWidget(self)
        widget.setLayout(formLayot)
        self.setWidget(widget)
        self.setWindowTitle("Aircondition")

    def update_temp_win(self,text):
        self.eLivRoomTemp.setText(text)
    def update_temp2_win(self, text):
        self.eRoomTemp.setText(text)    

class MainWindow(QMainWindow):
    
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
                
        # Init of Mqtt_client class
        # self.mc=Mqtt_client()
        self.mc=MC()
        
        # general GUI settings
        self.setUnifiedTitleAndToolBarOnMac(True)

        # set up main window
        self.setGeometry(30, 100, 800, 600)
        self.setWindowTitle('System GUI')        

        # Init QDockWidget objects        
        self.connectionDock = ConnectionDock(self.mc)        
        self.statusDock = StatusDock(self.mc)
        self.tempDock = TempDock(self.mc)
        self.graphsDock = GraphsDock(self.mc)
        self.airconditionDock= AirconditionDock(self.mc)

        self.addDockWidget(Qt.TopDockWidgetArea, self.connectionDock)
        self.addDockWidget(Qt.TopDockWidgetArea, self.tempDock)
        self.addDockWidget(Qt.TopDockWidgetArea, self.airconditionDock)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.statusDock)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.graphsDock)
       

app = QApplication(sys.argv)
mainwin = MainWindow()
mainwin.show()
app.exec_()
