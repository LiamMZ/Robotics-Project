#!/usr/bin/env python
import speech_recognition as sr
import time
import rospy
from std_msgs.msg import String

success = None

def callback_foundobjs(data):
    global success
    success = str(data.data) == "True"

def main():
    global success
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('SAY SOMETHING')
        audio = r.listen(source)
        print("TIME HAS RUN OUT, THANK YOU")

    try:
        word = r.recognize_google(audio)
        print("TEXT: " + word)
    except:
        pass;

    
    rospy.init_node('voicePub')
    pub = rospy.Publisher('/speech_recognition', String, queue_size=1)
    subscriber_foundobj = rospy.Subscriber('/foundObject', String, callback_foundobjs)
    # In case we need to loop
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        keys = ['bottle', 'cup']
        for i in word.split(' '):
            if i in keys:
                #print("That is a valid keyword!")
                pub.publish(i)
                time.sleep(7)
        if not success:
            print("Object Not Found!")
        else:
            print("Object Found!")

        rate.sleep()

if __name__ =="__main__":
    main()