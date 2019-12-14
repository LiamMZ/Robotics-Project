# ROS Portion
#!/usr/bin/env python
import rospy
from std_msgs.msg import String

rospy.init_node('voicePub')
pub = rospy.Publisher('/speech_recognition', String, queue_size=1)

keys = ['bottle', 'cup']

if any(x in word for x in keys):
    print("That is a valid keyword!")
    pub.publish(word)
else:
    print("ERROR: That is not a valid keyword")
