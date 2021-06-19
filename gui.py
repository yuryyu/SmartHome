import os
from sqlite3.dbapi2 import Date
import sys
import random
# pip install pyqt5-tools
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from matplotlib.pyplot import get
BASE_PATH = os.path.abspath(os.path.dirname(__file__))
from init import *
from agent import Mqtt_client 
import time
from icecream import ic
from datetime import datetime 
import data_acq as da
# pip install pyqtgraph
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg

global WatMet
WatMet=True
def time_format():
    return f'{datetime.now()}  GUI|> '
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
            global WatMet
            topic=msg.topic            
            m_decode=str(msg.payload.decode("utf-8","ignore"))
            ic("message from:"+topic, m_decode)
            if 'Room_1' in topic:
                mainwin.airconditionDock.update_temp_Room(m_decode.split('Temperature: ')[1].split(' Humidity: ')[0])
            if 'Common' in topic:            
                mainwin.airconditionDock.update_temp_Living_Room(m_decode.split('Temperature: ')[1].split(' Humidity: ')[0])
            if 'Home' in topic:               
                if WatMet:
                    mainwin.graphsDock.update_electricity_meter(m_decode.split('Electricity: ')[1].split(' Water: ')[0])
                    WatMet = False
                else:
                    mainwin.graphsDock.update_water_meter(m_decode.split(' Water: ')[1])
                    WatMet = True
            if 'alarm' in topic:            
                mainwin.statusDock.update_mess_win(da.timestamp()+': ' + m_decode)

   
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
        self.eConnectButton=QPushButton("Connect", self)
        self.eConnectButton.setToolTip("click me to connect")
        self.eConnectButton.clicked.connect(self.on_button_connect_click)
        self.eConnectButton.setStyleSheet("background-color: red")        
        formLayot=QFormLayout()
        formLayot.addRow("Host",self.eHostInput )
        formLayot.addRow("Port",self.ePort )        
        formLayot.addRow("",self.eConnectButton)
        widget = QWidget(self)
        widget.setLayout(formLayot)
        self.setTitleBarWidget(widget)
        self.setWidget(widget)     
        self.setWindowTitle("Connect") 
        
    def on_connected(self):
        self.eConnectButton.setStyleSheet("background-color: green")
        self.eConnectButton.setText('Connected')
            
    def on_button_connect_click(self):
        self.mc.set_broker(self.eHostInput.text())
        self.mc.set_port(int(self.ePort.text()))
        self.mc.set_clientName(self.eClientID.text())           
        self.mc.connect_to()        
        self.mc.start_listening()
        time.sleep(1)
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
        self.eRecMess=QTextEdit()
        self.eSubscribeButton = QPushButton("Subscribe",self)
        self.eSubscribeButton.clicked.connect(self.on_button_subscribe_click)       
        formLayot=QFormLayout()

        formLayot.addRow("", self.eStatusLivinigAirButton)
        formLayot.addRow("",self.eStatusRoomAirButton)
        formLayot.addRow("",self.eStatusBoilerButton)        
        formLayot.addRow("Alarm:",self.eRecMess)
        formLayot.addRow("",self.eSubscribeButton)        
                
        widget = QWidget(self)
        widget.setLayout(formLayot)
        self.setTitleBarWidget(widget)
        self.setWidget(widget)     
        self.setWindowTitle("Status") 
        
    def on_button_subscribe_click(self):        
        self.mc.subscribe_to(comm_topic+'alarm')
        self.eSubscribeButton.setStyleSheet("background-color: green")
    
    # create function that update text in received message window
    def update_mess_win(self,text):
        self.eRecMess.append(text)



              
       
    def on_button_publish_click(self):
        self.mc.publish_to(self.ePublisherTopic.text(), self.eMessageBox.toPlainText())
        self.ePublishButton.setStyleSheet("background-color: yellow")
        
class GraphsDock(QDockWidget):
    """Graphs """
    def __init__(self,mc):
        QDockWidget.__init__(self)        
        self.mc = mc        
        self.eElectricityButton = QPushButton("Show",self)
        self.eElectricityButton.clicked.connect(self.on_button_Elec_click)        
        self.eElectricityText=QLineEdit()
        self.eElectricityText.setText(" ")
        self.eWaterButton = QPushButton("Show",self)
        self.eWaterButton.clicked.connect(self.on_button_water_click)        
        self.eWaterText= QLineEdit()
        self.eWaterText.setText(" ")
        self.eDate= QLineEdit()
        self.eDate.setText("06-06-2021")
        self.eDateButton=QPushButton("Insert", self)
        self.eDateButton.clicked.connect(self.on_button_date_click)
        self.date=self.on_button_date_click
        formLayot=QFormLayout()       
        formLayot.addRow("Electricity meter",self.eElectricityButton)
        formLayot.addRow(" ", self.eElectricityText)
        formLayot.addRow("Water meter",self.eWaterButton)
        formLayot.addRow(" ", self.eWaterText)
        formLayot.addRow("Insert date: ", self.eDate)
        formLayot.addRow("", self.eDateButton)
        widget = QWidget(self)
        widget.setLayout(formLayot)
        self.setWidget(widget)
        self.setWindowTitle("Graphs")

    def update_water_meter(self, text):
        self.eWaterText.setText(text)

    def update_electricity_meter(self, text):
        self.eElectricityText.setText(text) 

    def on_button_date_click (self):
        dateStr= self.eDate.text()
        date=datetime.strptime(dateStr, '%d-%m-%Y')        
        return date

    def on_button_water_click(self):
       self.update_plot('2021-05-16','2021-05-21', 'WaterMeter')       
       self.eWaterButton.setStyleSheet("background-color: yellow")

    def on_button_Elec_click(self):
        self.update_plot('2021-05-16','2021-05-21', 'ElecMeter')
        self.eElectricityButton.setStyleSheet("background-color: yellow")

    def update_plot(self,date_st,date_end, meter):
        rez= da.filter_by_date('data',date_st,date_end, meter)
        temperature = []  
        timenow = []       
        for row in rez:
            timenow.append(row[1])
            temperature.append(float("{:.2f}".format(float(row[2]))))
        print(timenow)
        print(temperature)
        mainwin.plotsDock.plot(timenow, temperature) 

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

    def update_temp_Living_Room(self,text):
        self.eLivRoomTemp.setText(text)

    def update_temp_Room(self, text):
        self.eRoomTemp.setText(text)    

class PlotDock(QDockWidget):
    """Plots """
    def __init__(self):
        QDockWidget.__init__(self)        
        self.setWindowTitle("Plots")
        self.graphWidget = pg.PlotWidget()
        self.setWidget(self.graphWidget)
        rez= da.filter_by_date('data','2021-05-16','2021-05-18', 'ElecMeter')
        print(rez[1][0])
        # df = fetch_data(db_name,'data', 'WaterMeter')
        # ic2(df.head())
        datal = []  
        timel = []        
        for row in rez:
            timel.append(row[1])
            datal.append(float("{:.2f}".format(float(row[2]))))
        self.graphWidget.setBackground('b')
        # Add Title
        self.graphWidget.setTitle("Consuption Timeline", color="w", size="15pt")
        # Add Axis Labels
        styles = {"color": "#f00", "font-size": "20px"}
        self.graphWidget.setLabel("left", "Value (°C/m3)", **styles)
        self.graphWidget.setLabel("bottom", "Date (dd.hh/hh.mm)", **styles)
        #Add legend
        self.graphWidget.addLegend()
        #Add grid
        self.graphWidget.showGrid(x=True, y=True)
        #Set Range
        #self.graphWidget.setXRange(0, 10, padding=0)
        #self.graphWidget.setYRange(20, 55, padding=0)            
        pen = pg.mkPen(color=(255, 0, 0))
        self.data_line=self.graphWidget.plot( datal,  pen=pen)

    def plot(self, timel, datal):
        self.data_line.setData( datal)  # Update the data.

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
        self.plotsDock = PlotDock()
        self.addDockWidget(Qt.TopDockWidgetArea, self.connectionDock)
        self.addDockWidget(Qt.TopDockWidgetArea, self.tempDock)
        self.addDockWidget(Qt.TopDockWidgetArea, self.airconditionDock)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.statusDock)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.graphsDock)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.plotsDock)       

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwin = MainWindow()
    mainwin.show()
    app.exec_()
