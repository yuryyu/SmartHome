import time
from speech import *


class BOT():

    def bl(self,pl,st,ts):
        ts.save2file(ts.tts_request('Hello Itay. How do you do?'),ttsfile)
        
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
                ts.save2file(ts.tts_request('OK, goodby my good friend'),ttsfile)
                time.sleep(sys_delay)
                pl.play(ttsfile)
                time.sleep(sys_delay)
                return
            if 'no' in userresponcestring:            
                ts.save2file(ts.tts_request('OK, goodby my good friend'),ttsfile)
                time.sleep(sys_delay)
                pl.play(ttsfile)
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
            if "home" in userresponcestring:
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
                if "yes" in userresponcestring:
                    ts.save2file(ts.tts_request('The current state is: electricity operated in normal condition, water consuption is usial to seson and etc.'),ttsfile)
                    time.sleep(sys_delay)
                    pl.play(ttsfile)
                    time.sleep(sys_delay) 
                else :
                    ts.save2file(ts.tts_request('Ok, something else?'),ttsfile)
                    time.sleep(sys_delay)
                    pl.play(ttsfile)
                    time.sleep(sys_delay)
                continue
            if "room temperature" in userresponcestring:
                # here should be analitics request to manager
                print('Data request..')
                ts.save2file(ts.tts_request('The room temperature is 25 celcius degrees , whould you like to turn on the air conditioner ?'),ttsfile)
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
                    #time.sleep(sys_delay)
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
                        ts.save2file(ts.tts_request('OK, goodby my good friend'),ttsfile)
                        time.sleep(sys_delay)
                        pl.play(ttsfile)
                        time.sleep(sys_delay)
                    return 
                else :
                    #ts.save2file(ts.tts_request('Ok, something else?'),ttsfile)
                    #time.sleep(sys_delay)
                    pl.play("ok_something.wav")
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
                        ts.save2file(ts.tts_request('OK, goodby my good friend'),ttsfile)
                        time.sleep(sys_delay)
                        pl.play(ttsfile)
                        time.sleep(sys_delay)
                    return 
                continue
            if "electricity use" in userresponcestring:
            # here should be analitics request to manager
                print('Data request..')
                ts.save2file(ts.tts_request('You will want to see the electricity use in a daily, monthly or weekly view ?'),ttsfile)
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
                    pl.play("ok_something.wav")
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
                        ts.save2file(ts.tts_request('OK, goodby my good friend'),ttsfile)
                        time.sleep(sys_delay)
                        pl.play(ttsfile)
                        time.sleep(sys_delay)
                    return
                if 'monthly' in userresponcestring:
                    print('Data request..')
                    # here should be analitics request to manager
                    ts.save2file(ts.tts_request('montly report'),ttsfile)
                    time.sleep(sys_delay)
                    pl.play(ttsfile)
                    time.sleep(sys_delay)
                    pl.play("ok_something.wav")
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
                        ts.save2file(ts.tts_request('OK, goodby my good friend'),ttsfile)
                        time.sleep(sys_delay)
                        pl.play(ttsfile)
                        time.sleep(sys_delay)
                    return
                if 'weekly' in userresponcestring:
                    print('Data request..')
                    # here should be analitics request to manager
                    ts.save2file(ts.tts_request('weekly report'),ttsfile)
                    time.sleep(sys_delay)
                    pl.play(ttsfile)
                    time.sleep(sys_delay)
                    pl.play("ok_something.wav")
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
                        ts.save2file(ts.tts_request('OK, goodby my good friend'),ttsfile)
                        time.sleep(sys_delay)
                        pl.play(ttsfile)
                        time.sleep(sys_delay)
                    return
                else:
                    ts.save2file(ts.tts_request('Ok, something else?'),ttsfile)
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