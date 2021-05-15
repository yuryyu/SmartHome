import os
import sys
import random
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
BASE_PATH = os.path.abspath(os.path.dirname(__file__))
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
r=random.randrange(1,10000) # for creating unique client ID
clientname="IOT_clientId-nXLMZeDcjH"+str(r)


class MC(Mqtt_client):
    def __init__(self):
        super().__init__()

    def on_message(self, client, userdata, msg):
            topic=msg.topic
            m_decode=str(msg.payload.decode("utf-8","ignore"))
            ic("message from:"+topic, m_decode)            
            mainwin.subscribeDock.update_mess_win('Topic: '+ topic+' Message: '+ m_decode)

   
class ConnectionDock(QDockWidget):
    """Main """
    def __init__(self,mc):
        QDockWidget.__init__(self)
        
        self.mc = mc
        self.mc.set_on_connected_to_form(self.on_connected)
        
        self.eHostInput=QLineEdit()
        self.eHostInput.setInputMask('999.999.999.999')
        self.eHostInput.setText("139.162.222.115")
        
        self.ePort=QLineEdit()
        self.ePort.setValidator(QIntValidator())
        self.ePort.setMaxLength(4)
        self.ePort.setText("80")
        
        self.eClientID=QLineEdit()
        global clientname
        self.eClientID.setText(clientname)
        
        self.eUserName=QLineEdit()
        self.eUserName.setText("MATZI")
        
        self.ePassword=QLineEdit()
        self.ePassword.setEchoMode(QLineEdit.Password)
        self.ePassword.setText("MATZI")
        
        self.eKeepAlive=QLineEdit()
        self.eKeepAlive.setValidator(QIntValidator())
        self.eKeepAlive.setText("60")
        
        self.eSSL=QCheckBox()
        
        self.eCleanSession=QCheckBox()
        self.eCleanSession.setChecked(True)
        
        self.eConnectbtn=QPushButton("Connect", self)
        self.eConnectbtn.setToolTip("click me to connect")
        self.eConnectbtn.clicked.connect(self.on_button_connect_click)
        self.eConnectbtn.setStyleSheet("background-color: red")
        
        formLayot=QFormLayout()
        formLayot.addRow("Host",self.eHostInput )
        formLayot.addRow("Port",self.ePort )
        formLayot.addRow("Client ID", self.eClientID)
        formLayot.addRow("User Name",self.eUserName )
        formLayot.addRow("Password",self.ePassword )
        formLayot.addRow("Keep Alive",self.eKeepAlive )
        formLayot.addRow("SSL",self.eSSL )
        formLayot.addRow("Clean Session",self.eCleanSession )
        formLayot.addRow("",self.eConnectbtn)

        widget = QWidget(self)
        widget.setLayout(formLayot)
        self.setTitleBarWidget(widget)
        self.setWidget(widget)     
        self.setWindowTitle("Connect") 
        
    def on_connected(self):
        self.eConnectbtn.setStyleSheet("background-color: green")
        #self.eConnectbtn.setObjectName('Connected')
            
    def on_button_connect_click(self):
        self.mc.set_broker(self.eHostInput.text())
        self.mc.set_port(int(self.ePort.text()))
        self.mc.set_clientName(self.eClientID.text())
        self.mc.set_username(self.eUserName.text())
        self.mc.set_password(self.ePassword.text())        
        self.mc.connect_to()        
        self.mc.start_listening()
            
class PublishDock(QDockWidget):
    """Publisher """

    def __init__(self,mc):
        QDockWidget.__init__(self)
        
        self.mc = mc        
                
        self.ePublisherTopic=QLineEdit()
        self.ePublisherTopic.setText("matzi/iot_lesson")        
        self.eQOS=QComboBox()
        self.eQOS.addItems(["0","1","2"])       
        self.eRetainCheckbox = QCheckBox()
        self.eMessageBox=QPlainTextEdit()        
        self.ePublishButton = QPushButton("Publish_",self)
        
        formLayot=QFormLayout()        
        formLayot.addRow("Topic",self.ePublisherTopic)
        formLayot.addRow("QOS",self.eQOS)
        formLayot.addRow("Retain",self.eRetainCheckbox)
        formLayot.addRow("Message",self.eMessageBox)
        formLayot.addRow("",self.ePublishButton)
        
        self.ePublishButton.clicked.connect(self.on_button_publish_click)
        
        widget = QWidget(self)
        widget.setLayout(formLayot)
        self.setWidget(widget) 
        self.setWindowTitle("Publish")         
       
    def on_button_publish_click(self):
        self.mc.publish_to(self.ePublisherTopic.text(), self.eMessageBox.toPlainText())
        self.ePublishButton.setStyleSheet("background-color: yellow")
        
class SubscribeDock(QDockWidget):
    """Subscribe """

    def __init__(self,mc):
        QDockWidget.__init__(self)        
        self.mc = mc
        
        self.eSubscribeTopic=QLineEdit()
        self.eSubscribeTopic.setText("matzi/#") 
        
        self.eQOS = QComboBox()
        self.eQOS.addItems(["0","1","2"])
        
        self.eRecMess=QTextEdit()

        self.eSubscribeButton = QPushButton("Subscribe",self)
        self.eSubscribeButton.clicked.connect(self.on_button_subscribe_click)

        formLayot=QFormLayout()       
        formLayot.addRow("Topic",self.eSubscribeTopic)
        formLayot.addRow("QOS",self.eQOS)
        formLayot.addRow("Received",self.eRecMess)
        formLayot.addRow("",self.eSubscribeButton)
                
        widget = QWidget(self)
        widget.setLayout(formLayot)
        self.setWidget(widget)
        self.setWindowTitle("Subscribe")
        
    def on_button_subscribe_click(self):
        print(self.eSubscribeTopic.text())
        self.mc.subscribe_to(self.eSubscribeTopic.text())
        self.eSubscribeButton.setStyleSheet("background-color: yellow")
    
    # create function that update text in received message window
    def update_mess_win(self,text):
        self.eRecMess.append(text)
        
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
        self.publishDock =   PublishDock(self.mc)
        self.subscribeDock = SubscribeDock(self.mc)
        
        self.addDockWidget(Qt.TopDockWidgetArea, self.connectionDock)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.publishDock)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.subscribeDock)
       

app = QApplication(sys.argv)
mainwin = MainWindow()
mainwin.show()
app.exec_()
