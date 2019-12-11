import rospy
import intera_interface
from sawyer_pykdl import sawyer_kinematics

rospy.init_node("test_ik")
limb = intera_interface.Limb('right')
kinematics = sawyer_kinematics('right')
xyz_pos = [0.58, -0.48, 0.216]
x = dict(zip(limb._joint_names, kinematics.inverse_kinematics(xyz_pos)))
limb.move_to_joint_positions(x)
