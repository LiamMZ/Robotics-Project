import intera_interface
import rospy
import copy 
import time
import json
from geometry_msgs.msg import Pose2D
from std_msgs.msg import String

from geometry_msgs.msg import Pose, Point, Quaternion

g_limb = None
g_orientation_hand_down = None
g_position_neutral = None

end_pos = None

subscriber_voicerec = None
subscriber_foundobj = None
subscriber_objectLocation = None
target = None
foundObj = None
objLocationX = None
objLocationY = None

def callback_search_target(data):
    global target
    target = str(data.data)

def callback_found_obj(data):
    global foundObj
    foundObj = str(data.data) == "True"

def callback_object_location(data):
    global objLocationX, objLocationY
    objLocationX, objLocationY = data.x, data.y

def init():
    global g_limb, g_orientation_hand_down, g_position_neutral, end_pos
    rospy.init_node('motion')
    g_limb = intera_interface.Limb('right')

    #publisher/subscriber calls
    global subscriber_voicerec, subscriber_foundobj, subscriber_objectLocation
    #subscribe to speech_recognition
    subscriber_voicerec = rospy.Subscriber('/speech_recognition', String, callback_search_target)
    #subscribe to foundObject
    subscriber_foundobj = rospy.Subscriber('/foundObject', String, callback_found_obj)
    #subscribe to objectLocation
    subscriber_objectLocation = rospy.Subscriber('/objectLocation', Pose2D, callback_object_location)

    # This quaternion will have the hand face straight down (ideal for picking tasks)
    g_orientation_hand_down = Quaternion()
    g_orientation_hand_down.x = 0.704238785359
    g_orientation_hand_down.y =0.709956638597
    g_orientation_hand_down.z = -0.00229009932359
    g_orientation_hand_down.w = 0.00201493272073

    # This is the default neutral position for the robot's hand (no guarantee this will move the joints to neutral though)
    g_position_neutral = Point()
    g_position_neutral.x = 0.449559195663
    g_position_neutral.y = 0.16070379419
    g_position_neutral.z = 0.212938808947

    #set end location
    end_pos = Point()
    end_pos.x = 0.332647660893
    end_pos.y = 0.449912505313
    end_pos.z = 0.212938808947

def motion_options(target):
    global g_limb, g_position_neutral, g_orientation_hand_down, end_pos

    gripper = intera_interface.Gripper()
    gripper.open()

    '''
    # Create a new pose (Position and Orientation) to solve for
    target_pose = Pose()
    target_pose.position = copy.deepcopy(g_position_neutral)
    target_pose.orientation = copy.deepcopy(g_orientation_hand_down)
    '''
    interPose = Pose()
    target_pose = Pose()
    target_pose.orientation = copy.deepcopy(g_orientation_hand_down)

    if(target == "cup"):
        target_pose.position.x = 0.34 #some number
        target_pose.position.y = 0.0 #some number
        target_pose.position.z = 0.0824573129432
    elif(target == "bottle"):
        target_pose.position.x = 0.637622201808 #some number
        target_pose.position.y = -0.207056326819 #some number
        target_pose.position.z = 0.0824573129432
    elif(target == "bottle2"):
        target_pose.position.x = 0.721141027019 #some number
        target_pose.position.y = 0.162193976625 #some number
        target_pose.position.z = 0.0824573129432
    interPose = copy.deepcopy(target_pose)
    interPose.position.y+=.1
    interPose.position.z = 0.0824573129432
    # Call the IK service to solve for joint angles for the desired pose
    inter_joint_angles = g_limb.ik_request(interPose, "right_hand")
    target_joint_angles = g_limb.ik_request(target_pose, "right_hand")
    end_joint_angles = g_limb.ik_request(end_pos, "right_hand")

    # The IK Service returns false if it can't find a joint configuration
    if target_joint_angles is False:
        rospy.logerr("Couldn't solve for position %s" % str(target_pose))
        return

    # Set the robot speed (takes a value between 0 and 1)
    g_limb.set_joint_position_speed(0.2)

    # Send the robot arm to the joint angles in target_joint_angles, wait up to 2 seconds to finish
    g_limb.move_to_joint_positions(inter_joint_angles, timeout = 2)
    time.sleep(2)
    g_limb.move_to_joint_positions(target_joint_angles, timeout = 2)
    # Find the new coordinates of the hand and the angles the motors are currently at
    new_hand_pose = copy.deepcopy(g_limb._tip_states.states[0].pose)
    new_angles = g_limb.joint_angles()
    rospy.loginfo("New Hand Pose:\n %s" % str(new_hand_pose))
    rospy.loginfo("Target Joint Angles:\n %s" % str(target_joint_angles))
    rospy.loginfo("New Joint Angles:\n %s" % str(new_angles))

    #close gripper
    gripper.close()
    time.sleep(2)
    #return to neutral
    #g_limb.move_to_neutral()

    #move to end position
    g_limb.move_to_joint_positions(end_joint_angles)

    #open gripper
    gripper.open()


def main():
    global g_limb, g_position_neutral, g_orientation_hand_down

    global subscriber_voicerec, subscriber_foundobj, subscriber_objectLocation, target, foundObj, objLocationX, objLocationY

    init()

    # Move the arm to its neutral position
    g_limb.move_to_neutral()

    #rospy.loginfo("Old Hand Pose:\n %s" % str(g_limb._tip_states.states[0].pose))
    #rospy.loginfo("Old Joint Angles:\n %s" % str(g_limb.joint_angles()))
    
    # Create a new pose (Position and Orientation) to solve for
    #target_pose = Pose()
    #target_pose.position = copy.deepcopy(g_position_neutral)
    #target_pose.orientation = copy.deepcopy(g_orientation_hand_down)

    while not rospy.is_shutdown():
        if(foundObj):
            motion_options(target)
        else:
            pass
    

if __name__ == "__main__":
    main()