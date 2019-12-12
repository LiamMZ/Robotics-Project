
# coding: utf-8

# In[5]:


# requires portaudio to be installed as well as SpeechRecognition and pyaudio(Conda is best)
# Put this in the publisher?

import speech_recognition as sr

r = sr.Recognizer()

with sr.Microphone() as source:
    print('SAY SOMETHING');
    audio = r.listen(source)
    print("TIME IS UP FOR RECORDING")

try:
    word = r.recognize_google(audio)
    print("TEXT: " + word)
except:
    pass;


# In[6]:


# ROS Portion
#! /usr/bin/env python
 
import rospy
from std_msgs.msg import String
 
# rospy.init_node('voicePub')
 
# publisher = rospy.Publisher('/speech_recognition', String, queue_size=1)

# publisher.publish(word)
 

