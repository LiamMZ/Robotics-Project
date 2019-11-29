import rospy
import json
from geometry_msgs import Pose2D
from std_msgs.msg import String
from yolo_roboticsprj import ComputerVision

src = 1
subscriber_voicerec = None
publisher_foundobj = None
publisher_objloc = None
target = None


def callback_search_target(data):
    global target
    target = str(data)

def init():
    global subscriber_voicerec
    global publisher_foundobj, publisher_objloc
    
    subscriber_voicerec = rospy.Subscriber('/speech_recognition', String, callback_search_target)
    publisher_foundobj = rospy.Publisher('/foundObject', String, queue_size=10)
    publisher_objloc = rospy.Publisher('/objectLocation', Pose2D, queue_size=10)

def main():
    global subscriber_voicerec, target, src
    global publisher_objloc, publisher_foundobj
    args = {"config": "yolo3.cfg",
            "weights": "yolo3.weights",
            "classes": "yolo3.txt"}

    rospy.init_node("ComputerVision")
    init()
    CV = ComputerVision(args)
    cap = cv2.VideoCapture(src)
    while not rospy.is_shutdown():
        if target != None:
            ret, frame = cap.read()
            targetLoc = CV.findTarget(frame, target)
            if targetLoc[0]==-1:
                foundMSG = String()
                foundMSG.data = "False"
                publisher_foundobj.publish(foundMSG)
            else:
                foundMSG = String()
                foundMSG.data = "True"
                publisher_foundobj.publish(foundMSG)
                locMSG = Pose2D()
                locMSG.x = targetLoc[0]
                locMSG.y = targetLoc[1]
                locMSG.theta = 0
                publisher_objloc.publish(locMSG)
    cap.release()



if __name__=="__main__":
    main()