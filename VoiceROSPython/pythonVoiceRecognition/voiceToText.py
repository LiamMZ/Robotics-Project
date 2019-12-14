import speech_recognition as sr

r = sr.Recognizer()

with sr.Microphone() as source:
    print('SAY SOMETHING');
    audio = r.listen(source)
    print("TIME HAS RUN OUT, THANK YOU")

try:
    print("TEXT: " + r.recognize_google(audio))
except:
    pass;
