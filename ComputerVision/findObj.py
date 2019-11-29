import rospy
import json
from geometry_msgs import Pose2D
from std_msgs.msg import String
from yolo_roboticsprj import ComputerVision


subscriber_voicerec = None
publisher_foundobj = None
publisher_objloc = None
target = None


def callback_search_target(data):
    global target
    target = data

def init():
    global subscriber_voicerec
    global publisher_foundobj, publisher_objloc
    
    subscriber_voicerec = rospy.Subscriber('/speech_recognition', String, callback_search_target)
    publisher_foundobj = rospy.Publisher('/foundObject', String, queue_size=10)
    publisher_objloc = rospy.Publisher('/objectLocation', Pose2D, queue_size=10)

def main():
    global subscriber_voicerec, target
    global publisher_objloc, publisher_foundobj
    args = {"config": "yolo3.cfg",
            "weights": "yolo3.weights",
            "classes": "yolo3.txt"}

    rospy.init_node("ComputerVision")
    init()
    CV = ComputerVision(args)
    while not rospy.is_shutdown():
        if target != None:
            image = None
            targetLoc = CV.findTarget(image, target)



if __name__=="__main__":
    main()