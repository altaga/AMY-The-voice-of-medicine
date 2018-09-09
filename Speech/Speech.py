import gspread
from oauth2client.service_account import ServiceAccountCredentials
import speech_recognition as sr
from time import ctime
import time
import os
from gtts import gTTS

scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json',scope)
gc = gspread.authorize(creds)
# Open a worksheet from spreadsheet with one shot
sht1 = gc.open_by_key('1yTtiSksRKBtcks9mOr3rO8zB7OlellyPFetJrIY3MiI')
sht = sht1.get_worksheet(0)
r = sr.Recognizer()
m = sr.Microphone()
fase=0
name=""
edad=""
date=""
gen=""
doctor=""
months=""

def speak(fil):
    os.system("mpg321 "+ fil)

try:
    speak("saludo1.mp3")
    with m as source: r.adjust_for_ambient_noise(source)
    print("Set minimum energy threshold to {}".format(r.energy_threshold))
    while True:
        print("Say something!")
        with m as source: audio = r.listen(source)
        print("Got it! Now to recognize it...")
        try:
            value = r.recognize_google(audio)
            print(value[len(value)-1])
            print(value)
            if ((value[len(value)-1] == "s" and fase==0)):
                speak("desp1.mp3")
                fase=0
            elif ((value[len(value)-1] == "e" and fase==0)):
                speak("name1.mp3")
                fase=1
            elif (fase==1):                
                sht.update_acell('B1', value)
                speak("edalex1.mp3")
                fase=2
            elif (fase==2):
                sht.update_acell('B2', value)
                speak("birt1.mp3")
                fase=3
            elif (fase==3 and value[0] == "m"):
                sht.update_acell('B3', "Male")
                speak("gen1.mp3")
                fase=4
            elif (fase==3 and value[0] == "f"):
                sht.update_acell('B3', "Female")
                speak("gen1.mp3")
                fase=4
            elif (fase==4):
                sht.update_acell('B4', value)
                speak("doc1.mp3")
                fase=5
            elif (fase==5):
                sht.update_acell('B5', value)
                speak("mon1.mp3")
                fase=6
            elif (fase==6):
                sht.update_acell('B6', value)
                speak("1.mp3")
                fase=6
        except sr.UnknownValueError:
            print("Oops! Didn't catch that")
        except sr.RequestError as e:
            print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
except KeyboardInterrupt:
    pass