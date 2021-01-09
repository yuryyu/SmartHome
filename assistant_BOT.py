import time
from speech import *
import data_acq as da

class BOT():

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
                temperature = da.read_IOT_data('data', 'DHT-1')[-1][2]
                ts.save2file(ts.tts_request('The room temperature is ' + temperature + ' celcius degrees , whould you like to turn on the air conditioner ?'),ttsfile)
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
            

if __name__ == '__main__':
    pl = Player()
    st = STT()
    ts = TTS()
    print('Starting busyness logic example')
    bot = BOT()
    bot.bl(pl,st,ts)
    print('End of busyness logic example')