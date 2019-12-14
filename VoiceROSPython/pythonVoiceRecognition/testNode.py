#!/usr/bin/env python
import speech_recognition as sr

import rospy
from std_msgs.msg import String

r = sr.Recognizer()

with sr.Microphone() as source:
    print('SAY SOMETHING');
    audio = r.listen(source)
    print("TIME HAS RUN OUT, THANK YOU")

try:
    word = r.recognize_google(audio)
    print("TEXT: " + word)
except:
    pass;


rospy.init_node('voicePub')
pub = rospy.Publisher('/speech_recognition', String, queue_size=1)

# In case we need to loop
#rate = rospy.Rate(10)
#while not rospy.is_shutdown():
keys = ['bottle', 'cup']

if any(x in word for x in keys):
    print("That is a valid keyword!")
    pub.publish(word)
else:
    print("ERROR: That is not a valid keyword")

#    rate.sleep()
