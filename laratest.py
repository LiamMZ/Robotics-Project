import rospy
import json
from geometry_msgs.msg import Pose2D
from std_msgs.msg import String

publisher_voicerec = None
publisher_foundobj = None
publisher_objloc = None
target = None

def init():
    global publisher_voicerec
    global publisher_foundobj, publisher_objloc
    
    publisher_voicerec = rospy.Publisher('/speech_recognition', String, queue_size=10)
    publisher_foundobj = rospy.Publisher('/foundObject', String, queue_size=10)
    publisher_objloc = rospy.Publisher('/objectLocation', Pose2D, queue_size=10)

def main():
    global publisher_voicerec,target
    global publisher_foundobj, publisher_objloc

    rospy.init_node("TestNode")
    init()
    count = 0
    while not rospy.is_shutdown():
        if count == 0:
            
            testVoicerec = String()
            testVoicerec.data = "bottle"
            publisher_voicerec.publish(testVoicerec)

            testFoundObj = String()
            testFoundObj.data = "True"
            publisher_foundobj.publish(testFoundObj)
        


if __name__=="__main__":
    main()

