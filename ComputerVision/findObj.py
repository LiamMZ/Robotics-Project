import rospy
import cv2
import json
from geometry_msgs.msg import Pose2D
from std_msgs.msg import String
from yolo_roboticsprj import ComputerVision
from realPoseFromPixels import FindWorldPoseFromPixels

src = 0
subscriber_voicerec = None
publisher_foundobj = None
publisher_objloc = None
target = None


def callback_search_target(data):
    global target
    target = str(data.data)

def init():
    global subscriber_voicerec
    global publisher_foundobj, publisher_objloc
    
    subscriber_voicerec = rospy.Subscriber('/speech_recognition', String, callback_search_target)
    publisher_foundobj = rospy.Publisher('/foundObject', String, queue_size=10)
    publisher_objloc = rospy.Publisher('/objectLocation', Pose2D, queue_size=10)


def main():
    global subscriber_voicerec, target, src
    global publisher_objloc, publisher_foundobj
    args = {"config": "yolov3.cfg",
            "weights": "yolov3.weights",
            "classes": "yolov3.txt"}

    rospy.init_node("ComputerVision")
    init()
    CV = ComputerVision(args)
    cap = cv2.VideoCapture(src)
    while not rospy.is_shutdown():
        if target != None:
            _, frame = cap.read()
            target = target
            targetLoc = CV.findTarget(frame, target)
            if targetLoc[0]==-1:
                foundMSG = String()
                foundMSG.data = "False"
                publisher_foundobj.publish(foundMSG)
            else:
                foundMSG = String()
                foundMSG.data = "True"
                publisher_foundobj.publish(foundMSG)
                posConverter = FindWorldPoseFromPixels(frame)
                realPos = posConverter.calc_pose(targetLoc)
                locMSG = Pose2D()
                locMSG.x = realPos[0]
                locMSG.y = realPos[1]
                locMSG.theta = 0
                publisher_objloc.publish(locMSG)
    cap.release()



if __name__=="__main__":
    main()