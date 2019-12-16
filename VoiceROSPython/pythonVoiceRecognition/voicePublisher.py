# ROS Portion
#!/usr/bin/env python
import rospy
from std_msgs.msg import String

rospy.init_node('voicePub')
pub = rospy.Publisher('/speech_recognition', String, queue_size=1)

pub.publish(word)
