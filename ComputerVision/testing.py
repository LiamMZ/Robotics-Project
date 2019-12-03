import rospy
import json
from geometry_msgs import Pose2D
from std_msgs.msg import String

publisher_voicerec = None
subscriber_foundobj = None
subscriber_objloc = None
target = None

def init():
    global publisher_voicerec
    global subscriber_foundobj, subscriber_objloc
    
    publisher_voicerec = rospy.Publisher('/speech_recognition', String, queue_size=10)
    subscriber_foundobj = rospy.Subscriber('/foundObject', String, callback_foundobjs)
    subscriber_objloc = rospy.Subscriber('/objectLocation', Pose2D, callback_objloc)

def callback_foundobjs(data):
    print("######### foundobjs working: ", data)

def callback_objloc(data):
    print(data)

def main():
    global publisher_voicerec,target
    global subscriber_foundobj, subscriber_objloc

    rospy.init_node("TestNode")
    init()
    count = 0
    while not rospy.is_shutdown():
        if count == 0:
            testVoiceRec = String()
            testVoiceRec.data = "Person"
            publisher_voicerec.publish(testVoiceRec)
        


if __name__=="__main__":
    main()