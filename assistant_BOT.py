import time
from speech import *
from agent import Mqtt_client
from init import *
import random
global temperature
temperature = 0


r=random.randrange(1,10000000)
clientname="IOT_BOT-Id-"+str(r)

class BOT():
    def __init__(self, mc):
        self.mc=mc
        self.mc.set_broker(broker_ip)
        self.mc.set_port(int(port))
        self.mc.set_clientName(clientname)
        self.mc.set_username(username)
        self.mc.set_password(password)
        self.mc.on_message=self.on_BOT_message
        self.mc.on_connect=self.on_BOT_connect
        self.mc.on_disconnect=self.on_BOT_disconnect      
        self.mc.connect_to()        
        self.mc.start_listening()
        

    def bl(self,pl,st,ts):
        ts.save2file(ts.tts_request('Hello friend, how can i help you?'),ttsfile)
        
        time.sleep(sys_delay)
        # First greeting
        pl.play(ttsfile)
        time.sleep(sys_delay)    
        runit=True
        while runit:
            pl.record(userresponcefile)
            time.sleep(sys_delay)
            try:        
                userresponcestring = st.recognize(st.opensoundfile(userresponcefile)).results[0].alternatives[0].transcript
            except:
                userresponcestring  =''
            print(userresponcestring)
            time.sleep(1)
            if len(userresponcestring)==0:
                ts.save2file(ts.tts_request('Sorry, could you repeat, please?'),ttsfile)
                time.sleep(sys_delay)
                pl.play(ttsfile)
                time.sleep(sys_delay)        
                continue        
            if 'stop it' in userresponcestring:            
                time.sleep(sys_delay)
                pl.play("Goodbye.wav")
                time.sleep(sys_delay)
                return
            if 'no' in userresponcestring:            
                time.sleep(sys_delay)
                pl.play("Goodbye.wav")
                time.sleep(sys_delay)
                return
            if 'hi there' in userresponcestring:
                ts.save2file(ts.tts_request('What can I do for you, dear?'),ttsfile)
                time.sleep(sys_delay)
                pl.play(ttsfile)
                time.sleep(sys_delay)
                continue
            # if ("what's up" or "WhatsApp") in userresponcestring:
            #     ts.save2file(ts.tts_request('Nothing new, comrad'),ttsfile)
            #     time.sleep(sys_delay)
            #     pl.play(ttsfile)
            #     time.sleep(sys_delay)
            #     continue
            if "home status" in userresponcestring:
                # here should be analitics request to manager
                print('Data request..')
                ts.save2file(ts.tts_request('All systems are in normal state. Whould you like listen to report?'),ttsfile)
                time.sleep(sys_delay)
                pl.play(ttsfile)
                time.sleep(sys_delay)
                pl.record(userresponcefile)
                time.sleep(sys_delay)
                try:        
                    userresponcestring = st.recognize(st.opensoundfile(userresponcefile)).results[0].alternatives[0].transcript
                except:
                    userresponcestring  =''
                print(userresponcestring)
                if "yes" in userresponcestring:
                    ts.save2file(ts.tts_request('The current state is: electricity operated in normal condition, water consuption is usial to seson and etc.'),ttsfile)
                    time.sleep(sys_delay)
                    pl.play(ttsfile)
                    time.sleep(sys_delay)
                    pl.play("something else.wav")
                    time.sleep(sys_delay)
                    pl.record(userresponcefile)
                    time.sleep(sys_delay)
                    try:        
                        userresponcestring = st.recognize(st.opensoundfile(userresponcefile)).results[0].alternatives[0].transcript
                    except:
                        userresponcestring  =''
                    print(userresponcestring)
                    if 'yes' in userresponcestring: 
                        continue
                    else :
                        time.sleep(sys_delay)
                        pl.play("Goodbye.wav")
                        time.sleep(sys_delay)
                    return  
                else :
                    pl.play("something else.wav")
                    time.sleep(sys_delay)
                    pl.record(userresponcefile)
                    time.sleep(sys_delay)
                    try:        
                        userresponcestring = st.recognize(st.opensoundfile(userresponcefile)).results[0].alternatives[0].transcript
                    except:
                        userresponcestring  =''
                    print(userresponcestring)
                    if 'yes' in userresponcestring: 
                        continue
                    else :
                        time.sleep(sys_delay)
                        pl.play("Goodbye.wav")
                        time.sleep(sys_delay)
                    return 
                continue
            if "room temperature" in userresponcestring:
                # here should be analitics request to manager
                print('Data request..')
                temper=self.acq_temp()
                ts.save2file(ts.tts_request('The room temperature is '+ str(temper) +' celcius degrees , whould you like to turn on the air conditioner ?'),ttsfile)
                time.sleep(sys_delay)
                pl.play(ttsfile)
                time.sleep(sys_delay)
                pl.record(userresponcefile)
                time.sleep(sys_delay)
                try:        
                    userresponcestring = st.recognize(st.opensoundfile(userresponcefile)).results[0].alternatives[0].transcript
                except:
                    userresponcestring  =''
                print(userresponcestring)
                if "yes" in userresponcestring:
                    #ts.save2file(ts.tts_request('how many celcius degrees would you like to adjust the air?'),ttsfile)
                    #Check that the windows are close
                    pl.play("how_many_celcius.wav")
                    time.sleep(sys_delay)
                    pl.record(userresponcefile)
                    time.sleep(sys_delay) 
                    try:        
                        userresponcestring = st.recognize(st.opensoundfile(userresponcefile)).results[0].alternatives[0].transcript
                    except:
                        userresponcestring  =''
                    print(userresponcestring)
                    # here should be analitics request to manager
                    time.sleep(sys_delay)
                    print('Data request..')
                    ts.save2file(ts.tts_request('The air conditioner is set to ' +  str(userresponcestring) + 'degrees Celsius,something else?'),ttsfile)
                    time.sleep(sys_delay)
                    pl.play(ttsfile)
                    pl.record(userresponcefile)
                    time.sleep(sys_delay)
                    try:        
                        userresponcestring = st.recognize(st.opensoundfile(userresponcefile)).results[0].alternatives[0].transcript
                    except:
                        userresponcestring  =''
                    print(userresponcestring)
                    if 'yes' in userresponcestring: 
                        continue
                    else :
                        time.sleep(sys_delay)
                        pl.play("Goodbye.wav")
                        time.sleep(sys_delay)
                    return 
                else :
                    #ts.save2file(ts.tts_request('Ok, something else?'),ttsfile)
                    #time.sleep(sys_delay)
                    pl.play("something else.wav")
                    time.sleep(sys_delay)
                    pl.record(userresponcefile)
                    time.sleep(sys_delay)
                    try:        
                        userresponcestring = st.recognize(st.opensoundfile(userresponcefile)).results[0].alternatives[0].transcript
                    except:
                        userresponcestring  =''
                    print(userresponcestring)
                    if 'yes' in userresponcestring: 
                        continue
                    else :
                        time.sleep(sys_delay)
                        pl.play("Goodbye.wav")
                        time.sleep(sys_delay)
                    return 
                continue
            if "power consumption" in userresponcestring:
            # here should be analitics request to manager
                print('Data request..')
                ts.save2file(ts.tts_request('do you wish to see the daily,weekly or monthly power consumption report ?'),ttsfile)
                time.sleep(sys_delay)
                pl.play(ttsfile)
                time.sleep(sys_delay)
                pl.record(userresponcefile)
                time.sleep(sys_delay)
                try:
                   userresponcestring = st.recognize(st.opensoundfile(userresponcefile)).results[0].alternatives[0].transcript
                except:
                    userresponcestring  =''
                print(userresponcestring)
                if 'daily' in userresponcestring:
                    print('Data request..')
                    # here should be analitics request to manager
                    ts.save2file(ts.tts_request('daily report'),ttsfile)
                    time.sleep(sys_delay)
                    pl.play(ttsfile)
                    time.sleep(sys_delay)
                    pl.play("something else.wav")
                    time.sleep(sys_delay) 
                    pl.record(userresponcefile)
                    time.sleep(sys_delay)
                    try:        
                        userresponcestring = st.recognize(st.opensoundfile(userresponcefile)).results[0].alternatives[0].transcript
                    except:
                        userresponcestring  =''
                    print(userresponcestring)
                    if 'yes' in userresponcestring: 
                        time.sleep(sys_delay)
                        continue
                    else :
                        time.sleep(sys_delay)
                        pl.play("Goodbye.wav")
                        time.sleep(sys_delay)
                    return
                if 'monthly' in userresponcestring:
                    print('Data request..')
                    # here should be analitics request to manager
                    ts.save2file(ts.tts_request('montly report'),ttsfile)
                    time.sleep(sys_delay)
                    pl.play(ttsfile)
                    time.sleep(sys_delay)
                    pl.play("something else.wav")
                    time.sleep(sys_delay) 
                    pl.record(userresponcefile)
                    time.sleep(sys_delay)
                    try:        
                        userresponcestring = st.recognize(st.opensoundfile(userresponcefile)).results[0].alternatives[0].transcript
                    except:
                        userresponcestring  =''
                    print(userresponcestring)
                    if 'yes' in userresponcestring: 
                        continue
                    else :
                        time.sleep(sys_delay)
                        pl.play("Goodbye.wav")
                        time.sleep(sys_delay)
                    return
                if 'weekly' in userresponcestring:
                    print('Data request..')
                    # here should be analitics request to manager
                    ts.save2file(ts.tts_request('weekly report'),ttsfile)
                    time.sleep(sys_delay)
                    pl.play(ttsfile)
                    time.sleep(sys_delay)
                    pl.play("something else.wav")
                    time.sleep(sys_delay) 
                    pl.record(userresponcefile)
                    time.sleep(sys_delay)
                    try:        
                        userresponcestring = st.recognize(st.opensoundfile(userresponcefile)).results[0].alternatives[0].transcript
                    except:
                        userresponcestring  =''
                    print(userresponcestring)
                    if 'yes' in userresponcestring: 
                        continue
                    else :
                        time.sleep(sys_delay)
                        pl.play("Goodbye.wav")
                        time.sleep(sys_delay)
                    return
                else:
                    time.sleep(sys_delay)
                    pl.play("something else.wav")
                    time.sleep(sys_delay)
                continue
            if "water temperature" in userresponcestring:
            # here should be analitics request to manager
                print('Data request..')
                ts.save2file(ts.tts_request('The water temperature is 25 celcius degrees , whould you like to turn on the boiler ?'),ttsfile)
                time.sleep(sys_delay)
                pl.play(ttsfile)
                time.sleep(sys_delay)
                pl.record(userresponcefile)
                time.sleep(sys_delay)
                try:
                   userresponcestring = st.recognize(st.opensoundfile(userresponcefile)).results[0].alternatives[0].transcript
                except:
                    userresponcestring  =''
                print(userresponcestring)
                if 'yes' in userresponcestring:
                    print('Data request..')
                    # here should be analitics request to manager
                    ts.save2file(ts.tts_request('the boiler turned on'),ttsfile)
                    time.sleep(sys_delay)
                    pl.play(ttsfile)
                    time.sleep(sys_delay)
                    pl.play("something else.wav")
                    time.sleep(sys_delay) 
                    pl.record(userresponcefile)
                    time.sleep(sys_delay)
                    try:        
                        userresponcestring = st.recognize(st.opensoundfile(userresponcefile)).results[0].alternatives[0].transcript
                    except:
                        userresponcestring  =''
                    print(userresponcestring)
                    if 'yes' in userresponcestring: 
                        continue
                    else :
                        time.sleep(sys_delay)
                        pl.play("Goodbye.wav")
                        time.sleep(sys_delay)
                    return              
                else:
                    pl.play("something else.wav")
                    time.sleep(sys_delay)
                    pl.play(ttsfile)
                    time.sleep(sys_delay)
                continue
                time.sleep(sys_delay)

    def acq_temp(self):
        global temperature
        print(temperature)
        return temperature
        

    def on_BOT_message(self, client, userdata, msg):
        global temperature
        topic=msg.topic
        m_decode=str(msg.payload.decode("utf-8","ignore"))
        print("message from:"+topic, m_decode)
        temperature = float(m_decode.split('Temperature: ')[1].split(' Humidity')[0])


    def on_BOT_connect(self, client, userdata, flags, rc):        
        if rc==0:
            print("connected OK")                        
        else:
            print("Bad connection Returned code=",rc)
            
    def on_BOT_disconnect(self, client, userdata, flags, rc=0):        
        print("DisConnected result code "+str(rc))



if __name__ == '__main__':
    pl = Player()
    st = STT()
    ts = TTS()
    mc = Mqtt_client()
    # mc.client.on_message=on_BOT_message
    print('Starting busyness logic example')
    bot = BOT(mc)
    bot.bl(pl,st,ts)
    print('End of busyness logic example')