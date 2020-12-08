import time
from speech import *


class BOT():

    def bl(self,pl,st,ts):
        ts.save2file(ts.tts_request('Hello Yury. How do you do?'),ttsfile)
        #firstgreetingfile='C:\\Users\\yuzba\\Documents\\HIT\\Speech\\HandsOn6\\greeting.wav'
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
            if 'hi there' in userresponcestring:
                ts.save2file(ts.tts_request('What can I do for you, dear?'),ttsfile)
                time.sleep(sys_delay)
                pl.play(ttsfile)
                time.sleep(sys_delay)
                continue
            if "what's up" or "WhatsApp" in userresponcestring:
                ts.save2file(ts.tts_request('Nothing new, comrad'),ttsfile)
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