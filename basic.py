import rospy
import intera_interface
from sawyer_pykdl import sawyer_kinematics

rospy.init_node("ik")
limb = intera_interface.Limb("right")
kinematics = sawyer_kinematics("right")

import argparse 
parser = argparse.ArgumentParser(description="A tutorial of argparse!")

parser.add_argument("pos", default=[0, 0, 0, 0, 0, 0])

args = parser.parse_args()
a = args.a

joints = kinematics.inverse_kinematics(pos)
if(joints != None):
    dest = zip(limb._joint_names, joints)
    limb.move_to_joint_positions(dict(dest))
else:
    print("not a valid location")
